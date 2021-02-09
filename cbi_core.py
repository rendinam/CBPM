#
# Core communication data structures and methods for beam instrumentation
# control, acquisition, and support.
#

import re
from ctypes import *
from os import environ
import subprocess
from math import floor
import threading
import mpmnet

# Locate and load the cbi_net.so library for communications functions.
libdir = environ['ACC_RELEASE_DIR']+'/production/lib'
cbinet = CDLL(libdir+'/libcbi_net.so')

# Constants
MAX_CBI_NET_SINGLE_XFER_WORDS = 32000
CBI_6048_113_PKT_ADDR_TABLE = 0x10001000

# Module globals
#----------------
def camel_to_underscore(string):
    """Returns a copy of a CamelCased string to the
    underscore-separated equivalent.
    If the incoming string is not CamelCased, it is
    returned unchanged."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Centrally-managed list of instruments.  If uncaught exceptions
# lead to the interpreter exiting, all instruments in this
# list will have a potentially open socket closed gracefully.

class State():
    instrs = []
    
class AppState():
    timing_mode = None
    timing_setup = None

appstate = AppState()

# Reentrant Lock object for negotiating access to instruments
# as communication resources for sharing between background 
# status acquisition thread and any commands that are executed.
commlock = threading.RLock()


def ping(hostname):
    """Module-level function performs a quick single-packet
    ping to determine if a remote host is available via network.

    This employs the OS's command line ping program and examines
    its return code to determine if the ICMP echo request succeeded.

    Returns True if ping succeeded.
    Returns False if it did not."""
    pingproc = subprocess.Popen(['ping',
                                 '-c',
                                 '1',
                                 '-w',
                                 '1',
                                 '-q',
                                 hostname],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)
    out, error = pingproc.communicate()
    if pingproc.returncode == 0:
        return True
    else:
        return False



class ArrayProxy(object):
    """Class for creating proxy objects that provide a __setitem__
    override method so that communication structure objects can
    notice when their array-type contents are modified."""
    def __init__(self, array, struct):
        self.array = array
        self.struct = struct

    def __setitem__(self, i, val):
        self.array[i] = val
        self.struct.attributes_updated = True

    def __getitem__(self, i):
        item = self.array[i]
        if issubclass(type(item), Array):
            # Handle multidimensional arrays
            return ArrayProxy(item, self.struct)
        return item



class communication_struct(Structure):
    """Base class for all communication data structures.
    
    Defines the read() and write() methods on these structures."""
    
    # Var is common to all class instances formed.
    table_base = CBI_6048_113_PKT_ADDR_TABLE

    def __init__(self, socketfd):
        self.socketfd = socketfd
        self.table_addr = self.table_base + self.table_offset
        self.size_words = int(sizeof(self)/4)
        self.ptr = pointer(self)
        self.remote_addr = c_int()
        self.attributes_updated = False

    def __setattr__(self, name, value):
        '''Overload attribute setting method to toggle a flag
        indicating that the value of a particular communication structure
        simple attribute (not arrays) has been set since the last time the
        attribute "attributes_updated" has been cleared to False.'''
        super(communication_struct, self).__setattr__('attributes_updated', True)
        super(communication_struct, self).__setattr__(name, value)

    def __getattribute__(self, name):
        """Allow for proxy object to override __setitem__ attribute method
        so object can notice when its data is modified."""
        attr = super(communication_struct, self).__getattribute__(name)
        if issubclass(type(attr), Array):
            return ArrayProxy(attr, self)
        return attr

    def transfer(self, rw_switch, *wordstuple):
        """Transfers the contents of this communication data structure
        between the program's memory and the instrument's memory.
        The number of 32-bit words to transfer can be specified in the
        *wordstuple integer argument.  The entire structure will be
        transferred if this argument is absent.

        The developer shall use .read() and .write() instead of this
        method.
        
        The direction of the transfer from the program\'s perspective,
        either read or write, is specified as a string argument.

        This method is wrapped with the convenience methods
        .read() and .write() and is essentially private to this class.
        
        Will transfer the entire contents as a single cbi_net operation
        unless the payload size is greater than MAX_CBI_NET_SINGLE_XFER_WORDS.
        Then the total transfer is broken up into as many full maximum
        word transfers as possible, with the potential for a final, smaller
        remainder transfer."""
        
        # Maximum size of a single transfer in words
        # derived from MAX_REQ_BYTES in cbi_net_common.h
        packet_words = MAX_CBI_NET_SINGLE_XFER_WORDS
        
        # If the number of words to transfer was specified, set up to
        # transfer that many words.  Otherwise, set up to transfer the
        # contents of the entire structure.
        if len(wordstuple) > 0 and wordstuple[0] != 0:
            tot_words = wordstuple[0]
        else:
            tot_words = self.size_words        
        words_transferred = 0

        if tot_words < packet_words:
            packet_words = tot_words

        full_xfers = floor(tot_words / packet_words)
        
        fcns = {'read':cbinet.cbi_net_rd_mem,
                'write':cbinet.cbi_net_wr_mem}
        
        # Get address of remote structure from instrument's address table.
        cbinet.cbi_net_clr_error()
        try:
            ttransfer = cbinet.cbi_net_rd_mem(self.socketfd[0],
                                              self.table_addr,
                                              1,
                                              4,
                                              byref(self.remote_addr))
        except:
            # Catch IndexError here (socketfd has no entries, i.e. no connection)
            # And raise an IOError exception to be caught by caller.
            raise IOError
            
        if ttransfer == 0:
            cbinet.cbi_net_get_error.restype = c_char_p
            errmsg = cbinet.cbi_net_get_error()
            # This likely signifies that the DSP is not running. i.e. the
            # address table was never initialized.
            description = 'Error getting remote address (is processor running?)'+ bytes.decode(errmsg)
            raise IOError(description)

        # For incrementing of address values within this method, make
        # copies of the necessary pointers, one for remote structure
        # address, and one for the local structure pointer.
        remote_address_copy = self.remote_addr
        locptr = cast(self.ptr, POINTER(c_int))

        # Transfer all full cbi_net packet's worth of data.
        for xfer in range(0,full_xfers):
            cbinet.cbi_net_clr_error()
            ttransfer = fcns[rw_switch](self.socketfd[0],
                                        remote_address_copy,
                                        packet_words,
                                        4,
                                        locptr)
            if ttransfer == 0:
                errmsg = cbinet.cbi_net_get_error()
                raise IOError('Error in data xfer loop: address '+ str(errmsg))
            words_transferred = words_transferred + ttransfer
            # Increment remote address by one 32-bit word.
            remote_address_copy.value = remote_address_copy.value + packet_words
            # Increment local address by one 32-bit word.
            locptr = cast(addressof(locptr.contents)+(packet_words*4),
                          POINTER(c_int))

        # Transfer any remainder less than a full cbi_net packet's worth.
        if words_transferred != tot_words:
            leftover_words = tot_words - words_transferred
            cbinet.cbi_net_clr_error()
            ttransfer = fcns[rw_switch](self.socketfd[0],
                                        remote_address_copy,
                                        leftover_words,
                                        4,
                                        locptr)
            if ttransfer == 0:
                errmsg = cbinet.cbi_net_get_error()
                description = 'Error in remainder data xfer: '+ errmsg
                raise IOError(description)
            words_transferred = words_transferred + ttransfer


    def read(self, *wordstuple):
        """The number of 32-bit words to read from the instrument into local
        program memory can be specified as the only argument.
        The entire structure will be transferred if this argument is absent."""
        self.transfer('read', *wordstuple)


    def write(self, *wordstuple):
        """The number of 32-bit words to write from local program memory into
        the instrument's memory can be specified as the only argument.
        The entire structure will be transferred if this argument is absent."""
        self.transfer('write', *wordstuple)


        

class instrument_base():
    """Provides functionality common to all instruments."""
    def __init__(self):
        self.socketfd = []
        self.connected = False
        self.name = ''
        self.active = False
        self.error = False
    
    def connect(self):
        if len(self.socketfd) == 0:
            if ping(self.hostname):
                cbinet.cbi_net_clr_error()
                sfd = cbinet.cbi_net_fdopen(self.hostname_b)
                if sfd < 1:
                    cbinet.cbi_net_get_error.restype = c_char_p
                    errmsg = cbinet.cbi_net_get_error()
                    raise IOError( errmsg +' : '+self.hostname)
                self.socketfd.append(sfd)
                self.connected = True
            else:
                raise IOError('Unable to establish connection to hostname '+
                      self.hostname+' - ping failed.')
        else:
            print('INFO: Socketfd already obtained for '+ self.hostname)

    def disconnect(self):
        if len(self.socketfd) > 0:
            cbinet.cbi_net_clr_error()
            self.retstat = cbinet.cbi_net_close_socket(self.socketfd[0])
            if self.retstat == 0:
                cbinet.cbi_net_get_error.restype = c_char_p
                errmsg = cbinet.cbi_net_get_error()
                raise IOError('Error closing socket to '+self.hostname+': '+
                              bytes.decode(errmsg))
            cbinet.cbi_net_clr_error()
            cbinet.cbi_net_net_close(self.socketfd[0])            
            self.socketfd.pop()
            self.connected = False



def cleanup():
    mpmnet.disconnect()
    print('Disconnected from mpmnet.')
    for bpm in State.instrs:
        if bpm.connected:
            bpm.disconnect()
        print('Disconneced from',bpm.name)
    State.instrs = []
