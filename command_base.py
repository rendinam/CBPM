#
# command_base.py
#
#-*- python -*-
#
#

import time
import threading
import sys
import datetime
#import readline
from collections import OrderedDict

from cbpm import *
import appconfig


# TODO: Parse include files at commstruct generation time.
#       Generated a constants module to be imported.
class InstrumentCommands:
    CBI_INVALID_CMD_0 = 0
    CBI_IDLE_CMD = 1
    ACQUIRE_ALL_PEDESTALS_CMD = 2
    PEDESTAL_CAL_CMD = 3
    SET_GAINS_CMD = 4
    SET_DELAYS_CMD = 5
    RAW_DATA_CMD = 6
    PROC_DATA_CMD = 7
    CONT_DATA_CMD = 8
    BETATRON_PHASE_CMD = 9
    INJECTION_DATA_CMD = 10
    TEST_RAW_DATA_CMD = 11
    FIND_BUNCH_CMD = 12
    FIND_BTMD_CMD = 13
    TIME_SCAN_CMD = 14
    PUBLISH_TEMPS_CMD = 15
    SET_BUN_PAT_OFFSETS_CMD = 16
    SET_TIMING_MODE_CMD = 17
    CURRENT_DATA_CMD = 18
    CONTINUOUS_PROC_CMD = 19
    SET_TIMING_SETUP_CMD = 20
    CLEAR_DEBUG_CMD = 21
    
class InstHandshakes:
    CBI_ILLEGAL_HANDSHAKE_0 = 0
    CBI_CMD_NEW_HANDSHAKE = 1
    CBI_CMD_WORKING_HANDSHAKE = 2
    CBI_CMD_DONE_HANDSHAKE = 3
    CBI_CMD_ERROR_HANDSHAKE = 4
    CBI_CMD_TIMEOUT_HANDSHAKE = 5



class Prompt():
    def __init__(self):
        self.text = ''
        self.type = str
        self.destination = ''
        self.default = None
        self.choices = []
        self.mappings = {'n':0,
                         'N':0,
                         'y':1,
                         'Y':1,
                         'p':0,
                         'P':0,
                         'e':1,
                         'E':1}
        self.converter = None
        self.input_processor = None


class Command():
    """Command base class.  All BPM system commands inherit this."""

    inst_status_table = []

    def __init__(self):
        self.name = self.__class__.__name__
        # Create temporary bpm for populating with
        # command customization values.
        self.tbpm = BPM('TEMP')
        self.inst_command_code = None
        self.threads = []
        self.handshakes = {}
        self.connect = False
        self.force_connect = False
        self.prompts = []
        # Override in child class to set a different timeout period
        #   in seconds on a per-command basis.  This is the default
        #   for all commands.
        self.timeout = 4
        # Set all communication struct members (members with
        # an attribute "attributes_updated" to unmolested.
        for attribname, attrib in vars(self.tbpm).items():
            if isinstance(attrib, communication_struct):
                attrib.attributes_updated = False

    def init(self):
        self.__init__()

    def get_status_table(self):
        return self.inst_status_table

    def prompt(self):
        """Cycle through defined parameters, prompting the user via
        terminal to provide values."""
        assignments = {}
        for prompt in self.prompts:
            invalid_response = True
            while(invalid_response):
                invalid_response = False
                text = prompt.text
                # Present any list of choices as part of prompt.
                if len(prompt.choices) > 0:
                    text = text + ' ('
                    for choice in prompt.choices:
                        text = text + str(choice)
                        if choice != prompt.choices[-1]:
                            text = text + ','
                    text = text + ')'
                    text = text + '['+str(prompt.default)+']: '
                value = input(text)
                # Handle empty response
                if value.strip() == '':
                    value = prompt.default
                try:
                    value = prompt.type(value)
                except ValueError:
                    print('Invalid type')
                    invalid_response = True
                    continue
                if len(prompt.choices) > 0 \
                       and value not in prompt.choices \
                       and value != prompt.default:
                    print('  Not a choice')
                    invalid_response = True

                
            dest = prompt.destination

            if value in prompt.mappings:
                storeval = prompt.mappings[value]
            else:
                storeval = value
            assignments[dest] = storeval
            
        return assignments

    def set_param(self, object, chain, value):
        """Recursive method accepts a list of attribute names
        describing a chain linking one or more nested objects
        ending in an attribute which shall be set to a provided
        value.
        
        The second argument is the object which has the first
        item in the passed-in attribute chain as an attribute.
        
        The third argument is the value to assign to the last
        attribute in the chain."""
        if len(chain) == 1:
            setattr(object, chain[0], value)
        else:
            obj = getattr(object, chain[0])
            self.set_param(obj, chain[1:], value)

    def set_parameters(self, assignments):
        """For each attribute chain:value mapping provided
        in the dictionary 'mappings', calls the set_param
        method to assign the value to the (potentially nested)
        attribute specified."""
        for assignment in assignments:
            chain = assignment.split('.')
            self.set_param(self, chain, assignments[assignment])

    def initiate_remote_command(self, bpm):
        self.tbpm.cmd.cmd = self.inst_command_code
        self.tbpm.cmd.handshake = InstHandshakes.CBI_CMD_NEW_HANDSHAKE
        self.tbpm.cmd.cmd_status = InstHandshakes.CBI_ILLEGAL_HANDSHAKE_0
        # Copy C structure component from temporary staging instrumetn (tbpm)
        # to an actual instrument with an associated communications socket (bpm).
        pointer(getattr(bpm, 'cmd'))[0] = self.tbpm.cmd
        # Execute remote command.
        bpm.cmd.write()

    def check_handshake(self, bpm):
        start_time = time.time()
        if bpm.active:
            bpm.cmd.read()
            while bpm.cmd.handshake == InstHandshakes.CBI_CMD_NEW_HANDSHAKE \
                      or bpm.cmd.handshake == InstHandshakes.CBI_CMD_WORKING_HANDSHAKE:
                bpm.cmd.read()
                elapsed_time = time.time() - start_time
                if elapsed_time > self.timeout:
                    self.handshakes[bpm.name] = 'timeout'
                    return
                time.sleep(0.1)
                print('.',end='')
                sys.stdout.flush()
            if bpm.cmd.handshake == InstHandshakes.CBI_CMD_DONE_HANDSHAKE:
                self.handshakes[bpm.name] = 'done'
            if bpm.cmd.handshake == InstHandshakes.CBI_CMD_ERROR_HANDSHAKE:
                self.handshakes[bpm.name] = 'error'
                bpm.error = 'handshake error'

    def run(self, *self_contained):
        """Main command method. Responsible for propagating command parameter defaults
        and user input values to all active instruments, executing a remote command (if
        specified), and obtaining the results of the remote command."""
        print('Command '+self.name+' "run" method @ '+str(datetime.datetime.now()))

        # Acquire thread lock to allow sharing of instrument communications resources.
        commlock.acquire()

        # Allow for communication with instruments during prep stages, or in
        # the case where the command needs to talk to the instrument, but
        # does not need to send updated commstruct contents.
        if self.force_connect:
            for bpm in [b for b in State.instrs if b.active]:
                if bpm.error:
                    print(bpm.name +'-'+bpm.error)
                    continue
                try:
                    bpm.connect()
                except:
                    bpm.error = 'connect (1) error'

        # PREP stage (Only one of these is executed.)
        if 'prep' in dir(self):
            try:
                self.prep()
            except:
                bpm.error = 'prep error'

        if 'user_prep' in dir(self) and not self_contained and not appconfig.backend_mode:
            try:
                self.user_prep()
            except:
                bpm.error = 'user_prep error'

        # TODO: else gui_prep here?

        # Check if any commstructs need to be sent.  If so, open
        # a connection to all active instruments.
        for commstructname, commstruct in vars(self.tbpm).items():
            if isinstance(commstruct, communication_struct):
                if getattr(commstruct, 'attributes_updated'):
                    self.connect = True
                    break

        # Copy the C struct portion of every commstruct object modified in the
        # command's prep or user_prep phases to each active instrument.
        for bpm in [b for b in State.instrs if b.active and not b.error]:
            if self.connect and not bpm.connected:
                try:
                    bpm.connect()
                except:
                    bpm.error = 'connect (2) error'
            for commstructname, commstruct in vars(self.tbpm).items():
                if isinstance(commstruct, communication_struct):
                    if getattr(commstruct, 'attributes_updated'):
                        pointer(getattr(bpm, commstructname))[0] = commstruct
                        getattr(bpm, commstructname).write()

        # Initiate remote command if necessary.
        if self.inst_command_code:
            for bpm in [b for b in State.instrs if b.active and not b.error]:
                try:
                    self.initiate_remote_command(bpm)
                except:
                    bpm.error = 'initiate error'

        # Check handshake stage - Threaded approach
        if self.inst_command_code:
            for bpm in [b for b in State.instrs if b.active and not b.error]:
                thread = threading.Thread(target=self.check_handshake, args=(bpm,))
                self.threads.append(thread)
                thread.start()
        for thread in self.threads:
            thread.join()
        self.threads = []

        # Parallel Post (ppost) stage - Threaded approach
        if 'ppost' in dir(self):
            for bpm in [b for b in State.instrs if b.active and not b.error]:
                thread = threading.Thread(target=self.ppost, args=(bpm,))
                self.threads.append(thread)
                self.threads[-1].start()
            for thread in self.threads:
                thread.join()
            self.threads = []

        # Serial post (post) stage - non-threaded
        if 'post' in dir(self):
            for bpm in [b for b in State.instrs if b.active and not b.error]:
                if self.inst_command_code and self.handshakes[bpm.name] == 'done':
                    try:
                        self.post()
                    except:
                        bpm.error = 'post error'
                    
        [b.disconnect() for b in State.instrs if b.active and b.connected]

        self.inst_status_table = []
        if 'final' in dir(self):
            self.final()

        #if not appconfig.backend_mode and 'front_final' in dir(self):
        #    self.front_final()

        self.handshakes = {}

        # Release thread lock to allow sharing of instrument communication resources.
        commlock.release()
