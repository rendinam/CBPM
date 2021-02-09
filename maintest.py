#!/nfs/acc/libs/Linux_x86_64_intel/extra/bin/python3
#-*- python -*-
#
# maintest
#
from sys import exit
#from signal import *
import signal
import copy
from socket import gethostname, gethostbyname
import argparse
from configparser import ConfigParser, BasicInterpolation
#import readline
import atexit
import Pyro4

from cbpm import *
from commands import *
from user_io import *
from file_io import *


registered_names = []
nameserver = None

#for sig in (SIGINT):


def cleanit():
    print('Cleaning up...')
    cleanup()
    # De-register all pyro objects registered in this session.
    print('De-registering objects from nameserver...')
    for name in registered_names:
        nameserver.remove(name)

#signal(SIGINT, cleanit)

class Backend(object):
    def __init__(self):
        self.name = ''
        self.commands = []
        self.status_link_ids = []

    def get_name(self):
        return self.name

    def get_command_names(self):
        return self.commands


def initialize_bpm(name):
    config = ConfigParser(allow_no_value=True, strict=False)
    config.read(appconfig.inst_params_file)
    if config == None:
        print('ERROR reading BPM configuration file: ' + appconfig.inst_params_file)
    hostname = config[name]['hostname']
    bpm = BPM(hostname)
    bpm.name = name
    try:
        bpm.connect()
    except:
        print('Error communicating with '+bpm.name, '('+bpm.hostname+')')
        bpm.error = 'comm error'
        return bpm
    bpm.ident.read()
    bpm.disconnect()
    bpm.active = True
    return bpm


def acquire_status():
    """periodically refresh the resident status data values for
    all active BPMs.
    Supports communication resource sharing with other threads
    via 'commlock' thread lock object."""
    global commlock
    while True:
        for bpm in [b for b in State.instrs if b.active and not b.error]:
            commlock.acquire()
            try:
                bpm.connect()
            except IOError:
                print('acquire_status() failed to connect to '+bpm.name)
                bpm.error = 'comm error'
                commlock.release()
                continue
            try:
                bpm.ident.read()
                bpm.heartbeat.read()
                bpm.module_config.read()
                bpm.timing_config.read()
            except IOError:
                print('acquire_status() failed to read data structures from '+bpm.name)
                bpm.error = 'comm error'
                commlock.release()
                continue
            bpm.disconnect()
            commlock.release()
        time.sleep(0.1)
    
    
def poll_mpm_request():
    # global mpmlock
    in_progress = False
    while True:
        if appconfig.server_mode:
            values = mpmnet.vxgetn('CBPM CONTROL', 1, 20)
            
            print(values)
            if values[1] == 0 and in_progress:
                in_progress = False
                print('NOT')
            if values[1] == 2 and not in_progress:
                print('Measurement requested!')
                in_progress = True
                test_data = TestData()
                test_data.run(True)
            if values[1] == 2 and in_progress:
                in_progress = False
                time.sleep(18)
            time.sleep(1)


class Server():
    UseSysExit = True
    
    def __init__(self):
        self.max_statpanels = 3
        self.statpanels_in_use = 0
        self.statpanels = []

    def get_statpanel_name(self):
        print('GET_STATPANEL_NAME')
        if self.statpanels_in_use < self.max_statpanels:
            self.statpanels_in_use = self.statpanels_in_use + 1
            return 'bpm_status'+str(self.statpanels_in_use)
        else:
            return None

    def close_statpanel_link(self):
        self.statpanels_in_use = self.statpanels_in_use - 1


class BpmStatus(object):
    def __init__(self):
        self.in_use = False
    
    def get_status_list(self):
        statlist = []
        for bpm in State.instrs:
            entry = {}
            entry['name'] = bpm.name
            entry['hostname'] = bpm.hostname
            entry['heartbeat'] = bpm.heartbeat.heartbeat
            entry['clock'] = bpm.heartbeat.timing_integrity
            entry['turns_seen'] = bpm.heartbeat.turns_seen
            entry['ipaddr'] = bpm.ident.ipaddr
            entry['main_fpga'] = float(str(bpm.ident.fpga_maj)+'.'+
                                       str(bpm.ident.fpga_min))
            entry['fpga_ids'] = []
            for card in range(CBPM_MAX_CARDS):
                entry['fpga_ids'].append(bpm.ident.fe_fpga_id[card])
            entry['build'] = bpm.module_config.build_timestamp
            entry['core_ver'] = bpm.module_config.core_comm_struct_rev
            entry['plat_ver'] = bpm.module_config.platform_comm_struct_rev
            statlist.append(entry)
        return statlist



def main():

    global nameserver
    #atexit.register(cleanit)

    # Collect command line arguments
    argparser = argparse.ArgumentParser(description='BPM server software')
    argparser.add_argument('-a',
                           action='store',
                           dest='allocation',
                           help='Name of predefined instrument allocation')
    argparser.add_argument('--backend',
                           action='store_true',
                           dest='backend_mode',
                           default=False,
                           help='Start program in backend mode and wait '
                           'for a frontend to connect.')
    argresults = argparser.parse_args()

    # Store command line arguments
    appconfig.allocation = argresults.allocation
    appconfig.backend_mode = argresults.backend_mode

    mpmnet_manager_type = 'BPM'
    print('Connecting to MPMnet manager type: '+ mpmnet_manager_type)
    mpmnet.connect(mpmnet_manager_type)


    config = ConfigParser(allow_no_value=True, strict=False)
    config.read(appconfig.allocations_file)
    if config == None:
        print('ERROR reading BPM configuration file: ' + appconfig.allocations_file)

    try:
        names = config[appconfig.allocation]['instruments'].split()
    except KeyError:
        print('Make sure allocation name exists in file: '+appconfig.allocations_file)
        sys.exit(1)
    
    for name in names:
        bpm = initialize_bpm(name)
        State.instrs.append(bpm)

    read_bpm_params = ReadBpmParams()
    read_bpm_params.run()
    
    push_inst_configurations()


    # Compose a set of available commands.
    command_set = []
    command_set.append(FindBTMD())
    command_set.append(ClearDebug())
    command_set.append(ReadBpmParams())
    command_set.append(SendTimingConfig())
    command_set.append(SetActiveTimingSetup())
    command_set.append(GetDebugInfo())
    command_set.append(DisplayStackTrace())
    command_set.append(SetActiveGain())
    command_set.append(TestData())
    command_set.append(RawData())
    command_set.append(TimeScan())
    command_set.append(InstrumentStatus())
    command_set.append(TestMPM_and_nesting())
    command_set.append(ErrorStatus())
    command_set.append(ToggleMpmPolling())
    command_set.append(Exit())

    # Remote object support setup
    Pyro4.config.HMAC_KEY = b'KEY'
    host_name = gethostname().split('.')[0]
    host_ipaddr = gethostbyname(host_name)
    Pyro4.config.HOST = host_ipaddr
    daemon = Pyro4.Daemon()

    # Attempt to connect to a remote object nameserver
    try:
        nameserver = Pyro4.locateNS()
        appconfig.remote_available = True
    except Pyro4.errors.NamingError:
        appconfig.remote_available = False
        print('\nRemote object nameserver was not found.')
        print('The following features are not available')
        print('  Remote status panel(s)')
        print('  Frontend control of backend processes')
        print('\nTo provide these features, please start')
        print('a nameserver via the command')
        print('    "pyro_nameserver"')
        print('in a new terminal session and then')
        print('restart this program.\n')

    if appconfig.remote_available:
        server = Server()
        uri = daemon.register(server)
        nameserver.register('server', uri)
        registered_names.append('server')

        # Create one object for each remote status display supported.
        # The maximum number of status connections is defined by 
        # Server.max_stat_panels.
        for num in range(server.max_statpanels+1):
            bpm_status = BpmStatus()
            uri = daemon.register(bpm_status)
            nameserver.register('bpm_status'+str(num), uri)
            registered_names.append('bpm_status'+str(num))


    if appconfig.backend_mode:

        backend_ID = 0
        backend = Backend()
        backend.name = str(backend_ID)+'_backend'
        
        uri = daemon.register(backend)
        nameserver.register(backend.name, uri)
        registered_names.append(backend.name)
        
        # Register all commands to be exported.
        for command in command_set:
            uri = daemon.register(command)
            objname = str(backend_ID)+'_'+command.name
            nameserver.register(objname, uri)
            registered_names.append(objname)
            backend.commands.append(objname)

        # Start Pyro4 request loop in a thread of its own.
        thread = threading.Thread(target=daemon.requestLoop)
        thread.setDaemon(True)
        thread.start()
        print('Backend ready.')

    else:
        if appconfig.remote_available:
            # Start Pyro4 request loop in a thread of its own.
            thread = threading.Thread(target=daemon.requestLoop)
            thread.setDaemon(True)
            thread.start()
        
        # Start acquitision thread for realtime status update
        st_thread = threading.Thread(target=acquire_status)
        st_thread.setDaemon(True)
        st_thread.start()

        # Establish MPM request server thread
        mpm_req_thread = threading.Thread(target=poll_mpm_request)
        mpm_req_thread.setDaemon(True)
        mpm_req_thread.start()

    Exit.UseSysExit = Server.UseSysExit
    Exit.EndProgram[0] = False
    while not Exit.EndProgram[0]:
        prompt_and_run_command(command_set)

#     import pdb; pdb.set_trace()
    cleanup()

def signal_handler(signal, frame):
    print('----------------------Ctrl-C!\n')
    sys.exit(0)

        
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        Server.UseSysExit = True
        main()
    finally:
        # If any exceptions thrown end up here without being resolved,
        # call the cbi-level socket cleanup function that attempts to
        # gracefully terminate all socket connections to instruments
        # that have been 'registered' in the management list ('State.instrs')
        # provided by the module 'cbi_core'.
        print('[Finally] Cleaning up.')
        cleanup()
    
