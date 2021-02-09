#
# commands.py
#
#-*- python -*-
#
from configparser import ConfigParser, BasicInterpolation
import matplotlib.pyplot as plot

from command_base import *
import bpm_constants as const
from file_io import *

INVALID_ROUTINE_0 = 0
ACQUIRE_ALL_PEDESTALS_ID = 1
ADD_DEBUG_ID = 2
AUTO_GAIN_ID = 3
BACKUP_MATRIX_ID = 4
BUNCH_PATTERN_REDUCE_ID = 5
BUNCH_PATTERN_REDUCE_4NS_ID = 6
BUNCH_PATTERN_POST_ID = 7
CAL_LOC_OFFSET_ID = 8
CBPM_GET_ERRORS_ID = 9
CBPM_SET_ERROR_ID = 10
CHAN_DELAY_CAL_ID = 11
CHECK_RAW_BUF_ID = 12
CHECK_VALIDITY_ID = 13
CLEAR_DEBUG_ID = 14
COEFF_MATRIX_ID = 15
COLLECT_ID = 16
COLLECT_ADC_ID = 17
COLLECT_PROC_ID = 18
COLLECT_RAW_ID = 19
DETERMINE_STAT_ID = 20
DECODE_STAT_ID = 21
DISPATCH_ID = 22
DO_BLOCK_SCAN_ID = 23
DO_CALIBRATION_ID = 24
DSP_SLEEP_TURNS_ID = 25
ENCODE_STAT_ID = 26
FIND_BTMD_ID = 27
FIND_BUNCH_ID = 28
FIND_DELAYS_ID = 29
FLOAT_ERR_CHECK_ID = 30
FLOAT_ERR_CLEAR_ID = 31
GET_BETATRON_PHASE_ID = 32 
GET_BITS_ID = 33
GET_CONTINUOUS_DATA_ID = 34
GET_PROC_DATA_ID = 35
GET_RAW_DATA_ID = 36
INIT_ID = 37
ITERATE_ID = 38
LOAD_BUNCH_PATTERN_ID = 39
LU_DECOMP_ID = 40
LU_SAVE_SOL_ID = 41
LU_SOLVE_ID = 42
MAIN_ID = 43
MAT_MULT_ID = 44
MEASURE_ADC_RMS_ID = 45
NORMAL_BETATRON_ID = 46
PEDESTAL_CAL_ID = 47
PERFORM_TEST_ID = 48
PERFORM_TEST_2INPUT_ID = 49
PROCESS_ADC_ID = 50
PROCESS_DATA_ID = 51
PUBLISH_TEMPS_ID = 52
ROTATE_BUNCH_PATTERN_ID = 53
SET_BITS_ID = 54
SET_DELAYS_ID = 55
SET_GAINS_ID = 56
SET_TIMING_MODE_ID = 57
SET_TIMING_SETUP_ID = 58
TEST_RAW_DATA_ID = 59
TIME_SCAN_ID = 60
TS_SET_BUFFER_CONTROL_ID = 61
TSX_CHAN_STAT_ID = 62
UPDATE_SOL_ID = 63

routines = {
    INVALID_ROUTINE_0 : "",
    ACQUIRE_ALL_PEDESTALS_ID :  "acquire_all_pedestals",
    ADD_DEBUG_ID :  "add_debug",
    AUTO_GAIN_ID :  "auto_gain",
    BACKUP_MATRIX_ID :  "backup_matrix",
    BUNCH_PATTERN_REDUCE_ID :  "bunch_pattern_reduce",
    BUNCH_PATTERN_REDUCE_4NS_ID :  "bunch_pattern_reduce_4nS",
    BUNCH_PATTERN_POST_ID :  "bunch_pattern_post",
    CAL_LOC_OFFSET_ID :  "cal_loc_offset",
    CBPM_GET_ERRORS_ID :  "cbpm_get_errors",
    CBPM_SET_ERROR_ID :  "cbpm_set_error",
    CHAN_DELAY_CAL_ID :  "chan_delay_cal",
    CHECK_RAW_BUF_ID :  "check_raw_buf",
    CHECK_VALIDITY_ID :  "check_validity",
    CLEAR_DEBUG_ID :  "clear_debug",
    COEFF_MATRIX_ID :  "coeff_matrix",
    COLLECT_ID :  "collect",
    COLLECT_ADC_ID :  "collect_adc",
    COLLECT_PROC_ID :  "collect_proc",
    COLLECT_RAW_ID :  "collect_raw",
    DETERMINE_STAT_ID :  "determine_stat",
    DECODE_STAT_ID :  "decode_stat",
    DISPATCH_ID :  "dispatch",
    DO_BLOCK_SCAN_ID :  "do_block_scan",
    DO_CALIBRATION_ID :  "do_calibration",
    DSP_SLEEP_TURNS_ID :  "dsp_sleep_turns",
    ENCODE_STAT_ID :  "encode_stat",
    FIND_BTMD_ID :  "find_bTMD",
    FIND_BUNCH_ID :  "find_bunch",
    FIND_DELAYS_ID :  "find_delays",
    FLOAT_ERR_CHECK_ID :  "float_err_check",
    FLOAT_ERR_CLEAR_ID :  "float_err_clear",
    GET_BETATRON_PHASE_ID :  "get_betatron_phase",
    GET_BITS_ID :  "get_bits",
    GET_CONTINUOUS_DATA_ID :  "get_continuous_data",
    GET_PROC_DATA_ID :  "get_proc_data",
    GET_RAW_DATA_ID :  "get_raw_data",
    INIT_ID :  "init",
    ITERATE_ID :  "iterate",
    LOAD_BUNCH_PATTERN_ID :  "load_bunch_pattern",
    LU_DECOMP_ID :  "lu_decomp",
    LU_SAVE_SOL_ID :  "lu_save_sol",
    LU_SOLVE_ID :  "lu_solve",
    MAIN_ID :  "main",
    MAT_MULT_ID :  "mat_mult",
    MEASURE_ADC_RMS_ID :  "measure_adc_rms",
    NORMAL_BETATRON_ID :  "normal_betatron",
    PEDESTAL_CAL_ID :  "pedestal_cal",
    PERFORM_TEST_ID :  "perform_test",
    PERFORM_TEST_2INPUT_ID :  "perform_test_2input",
    PROCESS_ADC_ID :  "process_adc",
    PROCESS_DATA_ID :  "process_data",
    PUBLISH_TEMPS_ID :  "publish_temps",
    ROTATE_BUNCH_PATTERN_ID :  "rotate_bunch_pattern",
    SET_BITS_ID :  "set_bits",
    SET_DELAYS_ID :  "set_delays",
    SET_GAINS_ID :  "set_gains",
    SET_TIMING_MODE_ID :  "set_timing_mode",
    SET_TIMING_SETUP_ID :  "set_timing_setup",
    TEST_RAW_DATA_ID :  "test_raw_data",
    TIME_SCAN_ID :  "time_scan",
    TS_SET_BUFFER_CONTROL_ID :  "ts_set_buffer_control",
    TSX_CHAN_STAT_ID :  "tsx_chan_stat",
    UPDATE_SOL_ID :  "update_sol"
}


def push_inst_configurations():

    send_gain_config = SendGainConfig()
    send_gain_config.run()
    
    send_timing_config = SendTimingConfig()
    send_timing_config.run()

    set_active_gain = SetActiveGain()
    set_active_gain.run()

    set_active_timing_setup = SetActiveTimingSetup()
    set_active_timing_setup.run()
    


class FindBTMD(Command):
    def __init__(self):
        Command.__init__(self)
        


class ClearDebug(Command):
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.CLEAR_DEBUG_CMD
        self.force_connect = True



class ReadBpmParams(Command):
    """Read in from disk all the instrument-specific parameters for each allocated
    instrument and assign them to appropriate variables in that bpm."""
    def __init__(self):
        Command.__init__(self)
        self.force_connect = False
        self.gain_codes = []

    def prep(self):
        self.config = ConfigParser(allow_no_value=True, strict=False)
        self.config.read(appconfig.inst_params_file)
        if self.config == None:
            print('ERROR reading BPM configuration file: ' + appconfig.inst_params_file)
        codes = self.config['ALL_INSTRUMENTS']['gain_codes']
        for code in codes.split():
            self.gain_codes.append(code)

    def ppost(self, bpm):
        bpm.hostname = self.config[bpm.name]['hostname']
        for idx, code in enumerate(bpm.gain_config.gain_codes):
            bpm.gain_config.gain_codes[idx] = int(self.gain_codes[idx])
        for setupval, tsetup in enumerate(const.tsetup_names):
            vals = self.config[bpm.name][tsetup].split()                
            bpm.timing_config.setups[setupval].BP_offsets[0] = int(vals[0])
            bpm.timing_config.setups[setupval].BP_offsets[1] = int(vals[1])
            bpm.timing_config.setups[setupval].cTMD = int(vals[2])
            bpm.timing_config.setups[setupval].bTMDs[0] = int(vals[3])
            bpm.timing_config.setups[setupval].bTMDs[1] = int(vals[4])
            bpm.timing_config.setups[setupval].block_delays[0] = int(vals[5])
            bpm.timing_config.setups[setupval].block_delays[1] = int(vals[6])
            bpm.timing_config.setups[setupval].chan_delays[0][0] = int(vals[7])
            bpm.timing_config.setups[setupval].chan_delays[0][1] = int(vals[8])
            bpm.timing_config.setups[setupval].chan_delays[0][2] = int(vals[9])
            bpm.timing_config.setups[setupval].chan_delays[0][3] = int(vals[10])
            bpm.timing_config.setups[setupval].chan_delays[1][0] = int(vals[11])
            bpm.timing_config.setups[setupval].chan_delays[1][1] = int(vals[12])
            bpm.timing_config.setups[setupval].chan_delays[1][2] = int(vals[13])
            bpm.timing_config.setups[setupval].chan_delays[1][3] = int(vals[14])

        def read_table(key, destination):
            vals = self.config[bpm.name][key].split()
            count = 0
            for tblock in range(CBPM_MAX_TIMING_BLOCKS):
                for card in range(CBPM_MAX_CARDS):
                    for gsetting in range(CBPM_MAX_GAINS):
                        destination[tblock][card][gsetting] = float(vals[count])
                        count = count + 1
                        
        read_table('gain_table', bpm.gain_config.gain_table)
        read_table('4ns_e+_ped_table', bpm.pedestal_config.tables[0].ped_table)
        read_table('4ns_e-_ped_table', bpm.pedestal_config.tables[1].ped_table)
        read_table('14ns_ped_table', bpm.pedestal_config.tables[2].ped_table)



class SendTimingConfig(Command):
    """Transfer contents of timing configuration structures to instrument."""

    def __init__(self):
        Command.__init__(self)
        # Indicate that a connection shall be opened to each active instrument
        # so that configuration can be pushed since no structures will be touched
        # during a 'prep' stage.
        self.force_connect = True
    
    def ppost(self, bpm):
        try:
            bpm.timing_config.write()
        except IOError:
            bpm.error = True
            print('ERROR: Communication with '+bpm.name+' ('+bpm.hostname+') failed!')



class SendGainConfig(Command):
    """Transfer contents of gain configuration structures to instrument."""

    def __init__(self):
        Command.__init__(self)
        # Indicate that a connection shall be opened to each active instrument
        # so that configuration can be pushed since no structures will be touched
        # during a 'prep' stage.
        self.force_connect = True

    def prep(self):
        """TESTING - Populate gain table with all 1.0 values for testing purposes."""
        for tblock in range(CBPM_MAX_TIMING_BLOCKS):
            for card in range(CBPM_MAX_CARDS):
                for setting in range(CBPM_MAX_GAINS):
                    self.tbpm.gain_config.gain_table[tblock][card][setting] = 1.0

    def ppost(self, bpm):
        try:
            bpm.gain_config.write()
        except IOError:
            bpm.error = True
            print('ERROR: Communication with '+bpm.name+' ('+bpm.hostname+') failed!')

            

class SetActiveTimingSetup(Command):
    """Allows for the setting of the active timing
    setup used by an instrument.

    """# TODO: Must enforce all instruments to be in the same timing setup
    """state at all times to avoid confusion and potential for error.

    Enable all instruments that are not in an error state, change their
    active timing setup, then revert activations to previously found state."""
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.SET_TIMING_SETUP_CMD
        self.tbpm.op_timing.active_timing_setup = 5

    def ppost(self, bpm):
        bpm.op_timing.read()
        bpm.debug.read()
            


class GetDebugInfo(Command):
    """Retrieves and stack trace and instrument debug information
       from all active instruments."""
    def __init__(self):
        Command.__init__(self)
        # Indicate explicitly that a connection shall be opened to each active instrument
        # since no structures will be touched during a 'prep' stage.
        self.force_connect = True

    def ppost(self, bpm):
        bpm.stat.read()
        bpm.debug.read()



class DisplayStackTrace(Command):
    """Displays stack trace and debug information for all active instruments."""

    def final(self):
        for bpm in State.instrs:
            if bpm.active:
                idx = 0
                rid = bpm.stat.trace[idx]
                for rou in range(CBI_MAX_TRACE_LEVELS):
                    rid = bpm.stat.trace[rou]
                    if bpm.stat.num_levels == rou:
                        print('* ',end='')
                    else:
                        print('  ',end='')
                    if rid != 0:
                        print(routines[rid])
                    else:
                        break



class SetActiveGain(Command):
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.SET_GAINS_CMD
        for card in range(CBPM_MAX_CARDS):
            for tblock in range(CBPM_MAX_TIMING_BLOCKS):
                self.tbpm.op_gain.active_gain_settings[card][tblock] = 0


class TestData(Command):
    """Populate various instrument data structures with values
    and read them back for test purposes."""
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.TEST_RAW_DATA_CMD
        self.tbpm.diagnostic.magic_wait_calibration_value = 10
        self.tbpm.diagnostic.scrub_value = 666
        prompt = Prompt()
        prompt.text = 'Scrub value'
        prompt.type = int
        prompt.destination = 'tbpm.diagnostic.scrub_value'
        prompt.default = self.tbpm.diagnostic.scrub_value
        prompt.choices = [123,456,789]
        self.prompts.append(prompt)

    def user_prep(self):
        self.set_parameters(self.prompt())

    def ppost(self, bpm):
        vals = 1000
        bpm.adc_buffer0.read(vals)
        bpm.adc_buffer1.read(vals)
        bpm.adc_buffer2.read(vals)
        bpm.adc_buffer3.read(vals)
        bpm.adc_buffer4.read(vals)
        bpm.adc_buffer5.read(vals)
        bpm.adc_buffer6.read(vals)
        bpm.adc_buffer7.read(vals)
        
    def final(self):
        vals = 10
        for bpm in State.instrs:
            if bpm.active:
                print(bpm.name, bpm.hostname)
                for val in range(vals):
                    print(str(val)+')',
                          bpm.adc_buffer0.raw_data[val],
                          bpm.adc_buffer2.raw_data[val],
                          bpm.adc_buffer4.raw_data[val],
                          bpm.adc_buffer6.raw_data[val],
                          bpm.adc_buffer1.raw_data[val],
                          bpm.adc_buffer3.raw_data[val],
                          bpm.adc_buffer5.raw_data[val],
                          bpm.adc_buffer7.raw_data[val])
                print('')



class RawData(Command):
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.RAW_DATA_CMD
        self.tbpm.cmd_params.species = 0
        self.tbpm.cmd_params.bunch_pat[0] = 1
        self.tbpm.cmd_params.num_turns = 20
        self.tbpm.cmd_params.scale_mode = 0
        self.tbpm.cmd_params.trig_turns_delay = 0
        self.tbpm.cmd_params.spacex_turn = 0
        self.tbpm.cmd_params.use_data_enable = 0
        self.tbpm.cmd_params.trig_mask = 0

    def ppost(self, bpm):
        num_turns = self.tbpm.cmd_params.num_turns
        bpm.adc_buffer0.read(num_turns)
        bpm.adc_buffer1.read(num_turns)
        bpm.adc_buffer2.read(num_turns)
        bpm.adc_buffer3.read(num_turns)
        bpm.adc_buffer4.read(num_turns)
        bpm.adc_buffer5.read(num_turns)
        bpm.adc_buffer6.read(num_turns)
        bpm.adc_buffer7.read(num_turns)
        bpm.ph_word_buf.read(num_turns)
        bpm.debug.read()
        
    def final(self):
        test_data_file = '/home/mcr/devel/instr/pycbpm/OUT'
        open_data_file(test_data_file)
        write_cesr_header()
        for bpm in State.instrs:
            num_turns = self.tbpm.cmd_params.num_turns
            for turn in range(num_turns):
                write_data_fields(0,
                                  bpm.ph_word_buf.ph_words[turn],
                                  bpm.adc_buffer0.raw_data[turn],
                                  bpm.adc_buffer2.raw_data[turn],
                                  bpm.adc_buffer4.raw_data[turn],
                                  bpm.adc_buffer6.raw_data[turn])
        close_data_file()



class TimeScan(Command):
    """Scans on-board block delay values to get waveform representation
    data.  Parameters control whether or not the following occur:
      -Channel delays are adjusted
      -Waveform data is downloaded from instrument and plotted."""
    def __init__(self):
        Command.__init__(self)
        self.inst_command_code = InstrumentCommands.TIME_SCAN_CMD
        self.tbpm.cmd_params.species = 1
        self.tbpm.cmd_params.bunch_pat[0] = 1
        self.tbpm.cmd_params.delay_cal = 1
        self.tbpm.cmd_params.gain_cal = 0
        self.tbpm.cmd_params.trig_mask = 0
        self.tbpm.cmd_params.use_data_enable = 0
        self.tbpm.cmd_params.trig_mask = 0
        self.tbpm.find_delay_params.CalRadius = 10
        self.tbpm.find_delay_params.Block_Step = 1
        self.tbpm.cmd_params.generate_delay_corrections = 1
        self.plot_waveform = False
        
#         prompt = Prompt()
#         prompt.text = 'Species'
#         prompt.destination = 'tbpm.cmd_params.species'
#         prompt.default = 'p'
#         prompt.choices = ['p', 'e']
#         self.prompts.append(prompt)
        
#         prompt = Prompt()
#         prompt.text = 'Bunch'
#         prompt.destination = 'tbpm.cmd_params.bunch_pat'
        
        prompt = Prompt()
        prompt.text = 'Delay corrections?'
        prompt.destination = 'tbpm.cmd_params.generate_delay_corrections'
        prompt.default = 'y'
        prompt.choices = ['y', 'n']
        self.prompts.append(prompt)

        prompt = Prompt()
        prompt.text = 'Plot waveform?'
        prompt.destination = 'plot_waveform'
        prompt.default = 'n'
        prompt.mappings = {'y':True,
                           'Y':True,
                           'n':False,
                           'N':False}
        prompt.choices = ['y', 'n']
        self.prompts.append(prompt)

    def user_prep(self):
        self.set_parameters(self.prompt())
        # Query bunch

    def ppost(self, bpm):
        bpm.raw_data_header.read()
        num_turns = bpm.raw_data_header.num_turns
        # FIXME - instrument code needs to be modified to provide
        #         num_turns information in the raw_data header when
        #         performing a delay scan or adjustment.
        if num_turns == 0:
            print('num_turns in raw data header is 0! - setting to 16')
            num_turns = 16
        bpm.ident.read()
        bpm.cmd_params.read()
        bpm.find_delay_out.read()
        bpm.timing_config.read()
        if self.plot_waveform:
            bpm.adc_buffer0.read(800*num_turns)
            bpm.adc_buffer2.read(800*num_turns)
            bpm.adc_buffer4.read(800*num_turns)
            bpm.adc_buffer6.read(800*num_turns)

    def final(self):
        for bpm in State.instrs:
            print(bpm.name)
            print(bpm.find_delay_out.max_block_delay)
            print(bpm.find_delay_out.peaks[0],
                  bpm.find_delay_out.peaks[1],
                  bpm.find_delay_out.peaks[2],
                  bpm.find_delay_out.peaks[3])
            print(bpm.find_delay_out.offsets[0],
                  bpm.find_delay_out.offsets[1],
                  bpm.find_delay_out.offsets[2],
                  bpm.find_delay_out.offsets[3])
            if self.plot_waveform:
                print('bpm: ' + bpm.name)
                num_turns = bpm.raw_data_header.num_turns
                if num_turns == 0:
                    print('num_turns found to be zero!')
                    num_turns = 16
                xs = []
                card0 = []
                card1 = []
                card2 = []
                card3 = []
                data = [card0, card1, card2, card3]
                bufs = [bpm.adc_buffer0.raw_data,
                        bpm.adc_buffer2.raw_data,
                        bpm.adc_buffer4.raw_data,
                        bpm.adc_buffer6.raw_data]
                sums = [0,0,0,0]
                avgs = [0.0,0.0,0.0,0.0]
                for dstep in range(800):
                    xs.append(dstep)
                for card in range(CBPM_MAX_CARDS):
                    for dstep in range(800):
                        sums[card] = 0
                        avgs[card] = 0.0
                        for turn in range(num_turns):
                            idx = (dstep*num_turns) + turn
                            sums[card] = sums[card] + bufs[card][idx]
                        avgs[card] = sums[card] / num_turns
                        data[card].append(avgs[card])
                labels = ['TI', 'BI', 'BO', 'TO']
                for card in range(CBPM_MAX_CARDS):
                    plot.plot(xs,
                              data[card],
                              label=str(card)+' '+labels[card])
                    plot.legend()
                hostname = bytes.decode(bpm.ident.hostname)
                ipaddr = bytes.decode(bpm.ident.ipaddr)
                tsetup = appstate.timing_setup
                plot.suptitle('Block delay scan: '+bpm.name+ \
                              ' ('+hostname+') '+str(123))
                plot.show()
        print('\n\n\n   Timing Adjustment Summary:               \n')
        print('                          Card-to-card change      Absolute change on each card')
        print('                      (diff from c0 before/after)')
        print('BAD                                                   c0     c1     c2    c3')
        print('------------------------------------------------------------------------------------')
        for bpm in State.instrs:
            print('[ ] '+bpm.name, bpm.hostname)



class InstrumentStatus(Command):
    """Obtain all vital identification and configuration info from an instrument."""
    
    def __init__(self):
        Command.__init__(self)
        self.force_connect = True

    def ppost(self, bpm):
        bpm.heartbeat.read()
        bpm.ident.read()
        bpm.timing_config.read()

    def final(self):
        for bpm in [b for b in State.instrs if b.active]:
            self.inst_status_table.append(
                [bpm.name, bpm.hostname, bpm.heartbeat.turns_seen])
            print([bpm.name, bpm.hostname, bpm.heartbeat.turns_seen])



class TestMPM_and_nesting(Command):
    """Perform some transfers to/from the CESR MPM for testing purposes."""

    def prep(self):
        print('Nested command test...')
        instrument_status = InstrumentStatus()
        instrument_status.run()
    
    def final(self):
        print('Reading from MPM (CBPM CONTROL 1-20)...')
        values = mpmnet.vxgetn('CBPM CONTROL', 1, 20)
        print(values)

        print('Writing to MPM (CBPM ADR ALL 101)...')
        values = [268697602]
        mpmnet.vxputn('CBPM ADR ALL', 101, 101, values)

        print('Reading from MPM (CBPM ADR ALL 101)...')
        values2 = mpmnet.vxgetn('CBPM ADR ALL', 101, 101)
        print(values2)

        if values[0] == values2[0]:
            print('MPM accesses succeeded!')
        else:
            print('MPM accesses FAILED!')
        print('\n')
        


# class SaveTimingParams(Command):
#     """Makes an intermediate copy of the instrument parameters file.
#     Then replaces the timing values requested within that file."""


#class SelectActive(Command):


class ErrorStatus(Command):
    """Print a table of error status values for all instruments."""
    def prep(self):
        print('\n')
        for bpm in State.instrs:
            print(bpm.name, bpm.hostname, bpm.error)
        print('')


class ToggleMpmPolling(Command):
    """Turn the program's ability to honor measurement requests
    made via the MPM ON or OFF depending on the current state."""
    def final(self):
        if appconfig.server_mode == False:
            appconfig.server_mode = True
            print('Now honoring MPM requests')
        else:
            appconfig.server_mode = False
            print('MPM requests disabled')



class Exit(Command):
    """Exit the program."""
    
    EndProgram = [False]
    UseSysExit = True

    def final(self):
        print("Exiting...")
        self.EndProgram[0] = True
#         sys.exit(0)
        if self.UseSysExit:
            sys.exit(0)
