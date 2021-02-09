#----------------------------------------------
# Automatically generated python3 module code
# for core communication data structures.
#----------------------------------------------

from cbi_core import *

#---------------------------------------
# Necessary constants imported from
# header files.
#---------------------------------------
CBI_MAX_ERROR_WORDS = 4
CBI_MAX_TRACE_LEVELS = 15
CBI_MAX_DEBUG_WORDS = 660

#---------------------------------------
# Data type structures, used to compose
# various communication data structures.
#---------------------------------------
#---------------------------------------
# Communication data structure class
# definitions.
#---------------------------------------
class CMD(communication_struct):
    _fields_ = [('cmd', c_int),
                ('cmd_status', c_int),
                ('error', c_int*CBI_MAX_ERROR_WORDS),
                ('handshake', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 1
        communication_struct.__init__(self, socketfd)


class STAT(communication_struct):
    _fields_ = [('state', c_int),
                ('status', c_int),
                ('num_levels', c_int),
                ('trace', c_int*CBI_MAX_TRACE_LEVELS)]

    def __init__(self, socketfd):
        self.table_offset = 2
        communication_struct.__init__(self, socketfd)


class DEBUG(communication_struct):
    _fields_ = [('write_ptr', c_int),
                ('debug', c_int*CBI_MAX_DEBUG_WORDS),
                ('routine', c_int*CBI_MAX_DEBUG_WORDS),
                ('padding', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 3
        communication_struct.__init__(self, socketfd)


class IDENT(communication_struct):
    _fields_ = [('ipaddr', c_char*16),
                ('hostname', c_char*28),
                ('module_type', c_int),
                ('fpga_maj', c_int),
                ('fpga_min', c_int),
                ('fe_fpga_id', c_int*4)]

    def __init__(self, socketfd):
        self.table_offset = 4
        communication_struct.__init__(self, socketfd)


class HEARTBEAT(communication_struct):
    _fields_ = [('heartbeat', c_int),
                ('timing_integrity', c_int),
                ('turns_seen', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 5
        communication_struct.__init__(self, socketfd)


class MODULE_CONFIG(communication_struct):
    _fields_ = [('exe_type', c_int),
                ('exe_version', c_float),
                ('ldr_name', c_char*44),
                ('build_timestamp', c_int),
                ('core_comm_struct_rev', c_int),
                ('platform_comm_struct_rev', c_int),
                ('compiler_ver', c_int),
                ('lib_version', c_float),
                ('hardware_ver', c_int),
                ('firmware_ver', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 6
        communication_struct.__init__(self, socketfd)


class instrument(instrument_base):
    """Provides for instantiation of all core
    instrumentation communication structures."""
    def __init__(self, host):
        instrument_base.__init__(self)
        self.hostname = host
        self.hostname_b = str.encode(host)

        self.cmd = CMD(self.socketfd)
        self.stat = STAT(self.socketfd)
        self.debug = DEBUG(self.socketfd)
        self.ident = IDENT(self.socketfd)
        self.heartbeat = HEARTBEAT(self.socketfd)
        self.module_config = MODULE_CONFIG(self.socketfd)
