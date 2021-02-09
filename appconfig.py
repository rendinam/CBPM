#
# appconfig.py
#
#-*- python -*-
#
#

# For holding application-level configuration items.
#  paths, command preferences, etc
#
# Read a config file to populate these.

inst_params_file = './BPM_inst_params.new'
allocations_file = './allocations'

# Via flags from command line
allocation = None
backend_mode = False  # EXAMINE: Set in backend but not set in frontend,
                      # command's run() method depends on a value in
                      # both cases.

# State
remote_available = False
server_mode = False
