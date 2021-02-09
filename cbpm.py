#----------------------------------------------
# Automatically generated python3 module code
# for core communication data structures.
#----------------------------------------------

from cbi import *

#---------------------------------------
# Necessary constants imported from
# header files.
#---------------------------------------
CBPM_MAX_TIMING_BLOCKS = 2
CBPM_MAX_CARDS = 4
CBPM_MAX_GAINS = 11
CBPM_MAX_CHAN_DELAY_COUNTS = 1024
CBPM_MAX_TIMING_SETUPS = 6
CBPM_MAX_MULTIGAIN_SETUPS = 3
CBPM_ADC_BUF_USE = 327680
CBPM_MAX_BUNCHES = 640
CBPM_MAX_PROC_BUFS = 3
CBPM_MAX_AUTO_SAMPLES = 640
CBI_NUM_SPECIES = 2
CBPM_MAX_PHASE_JUMPS = 3
CBPM_NUM_DP_TURNS_OFFSET = 5
CBPM_HALF_TURN_OPTIONS = 2
CBPM_MAX_PHASE_DIM = 2
CBPM_NUM_PHASE_COEFFS = 2
CBPM_MAX_FIT_COEFFS = 12
CBPM_MAX_ACQ_CONTROLLERS = 4
CBPM_FIND_DELAYS_HIST_LENGTH = 8
CBPM_MAX_CHANS_PER_CARD = 2
CBPM_NUM_TESTS = 6
CBPM_MAX_NUM_EXECUTION_FLAGS = 20
CBPM_NUM_TESTS_ENCODED = 6

#---------------------------------------
# Data type structures, used to compose
# various communication data structures.
#---------------------------------------
class TSETUP(communication_struct):
    _fields_ = [('timing_mode', c_int),
                ('cTMD', c_int),
                ('BP_offsets', c_int*CBPM_MAX_TIMING_BLOCKS),
                ('bTMDs', c_int*CBPM_MAX_TIMING_BLOCKS),
                ('block_delays', c_int*CBPM_MAX_TIMING_BLOCKS),
                ('chan_delays', (c_int*CBPM_MAX_CARDS)*CBPM_MAX_TIMING_BLOCKS)]

class PEDESTALS(communication_struct):
    _fields_ = [('ped_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_TIMING_BLOCKS),
                ('ped_rms_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_TIMING_BLOCKS)]

class PROC_DATA(communication_struct):
    _fields_ = [('msmt_and_bun_id', c_int),
                ('data_counter', c_int),
                ('turn_counter', c_int),
                ('signal', c_float*CBPM_MAX_CARDS),
                ('signal_rms', c_float*CBPM_MAX_CARDS)]

class SUMM_DATA(communication_struct):
    _fields_ = [('gain', c_int*CBPM_MAX_CARDS),
                ('delay', c_int),
                ('chan_delay', c_int),
                ('signal', c_float*CBPM_MAX_CARDS)]

class CHAN_CAL_DATA(communication_struct):
    _fields_ = [('data', c_float*CBPM_MAX_CHAN_DELAY_COUNTS),
                ('error', c_float*CBPM_MAX_CHAN_DELAY_COUNTS)]

class TEST_PARAMS_STRUCT(communication_struct):
    _fields_ = [('type', c_int),
                ('error_threshold', c_float),
                ('warning_threshold', c_float),
                ('enable', c_int),
                ('required_for_update_acceptance', c_int)]

#---------------------------------------
# Communication data structure class
# definitions.
#---------------------------------------
class CMD_PARAMS(communication_struct):
    _fields_ = [('species', c_int),
                ('num_turns', c_int),
                ('bunch_pat', c_int*40),
                ('rot_bunch_pat', c_int*640),
                ('trig_turns_delay', c_int),
                ('spacex_turn', c_int),
                ('delay_cal', c_int),
                ('generate_delay_corrections', c_int),
                ('gain_cal', c_int),
                ('gain_xcal', c_int),
                ('avg_mode', c_int),
                ('scale_mode', c_int),
                ('update_mode', c_int),
                ('use_data_enable', c_int),
                ('trig_mask', c_int),
                ('reset_proc_buf_idx', c_int),
                ('generate_phase_tables', c_int),
                ('tblock', c_int),
                ('bun_pat_offset', c_int),
                ('checksum', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 7
        communication_struct.__init__(self, socketfd)


class TEMPERATURES(communication_struct):
    _fields_ = [('dig_temp', c_float),
                ('tim_temp', c_float),
                ('fe_temps', c_float*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 8
        communication_struct.__init__(self, socketfd)


class TIMING_CONFIG(communication_struct):
    _fields_ = [('setups', TSETUP*CBPM_MAX_TIMING_SETUPS)]

    def __init__(self, socketfd):
        self.table_offset = 9
        communication_struct.__init__(self, socketfd)


class GAIN_CONFIG(communication_struct):
    _fields_ = [('gain_codes', c_int*CBPM_MAX_GAINS),
                ('gain_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_TIMING_BLOCKS),
                ('gain_err_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_TIMING_BLOCKS),
                ('chan_map', c_int*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 10
        communication_struct.__init__(self, socketfd)


class PEDESTAL_CONFIG(communication_struct):
    _fields_ = [('tables', PEDESTALS*CBPM_MAX_MULTIGAIN_SETUPS)]

    def __init__(self, socketfd):
        self.table_offset = 11
        communication_struct.__init__(self, socketfd)


class OP_TIMING(communication_struct):
    _fields_ = [('active_timing_setup', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 12
        communication_struct.__init__(self, socketfd)


class OP_GAIN(communication_struct):
    _fields_ = [('active_gain_settings', (c_int*CBPM_MAX_TIMING_BLOCKS)*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 13
        communication_struct.__init__(self, socketfd)


class RAW_DATA_HEADER(communication_struct):
    _fields_ = [('tot_bunches', c_int),
                ('num_bunches', c_int*CBPM_MAX_TIMING_BLOCKS),
                ('num_BP_bits_wrapped', c_int*CBPM_MAX_TIMING_BLOCKS),
                ('num_turns', c_int),
                ('skip_turns_active', c_int),
                ('turn_counter', c_int),
                ('trig_turns_delay', c_int),
                ('spacex_turn', c_int),
                ('scale_mode', c_int),
                ('ADC_zero_val_bitfields', c_int*CBPM_MAX_CARDS),
                ('ADC_lower_thresh_bitfields', c_int*CBPM_MAX_CARDS),
                ('ADC_low_thresh_bitfields', c_int*CBPM_MAX_CARDS),
                ('ADC_high_thresh_bitfields', c_int*CBPM_MAX_CARDS),
                ('ADC_saturation_bitfields', c_int*CBPM_MAX_CARDS),
                ('gain', (c_int*CBPM_MAX_TIMING_BLOCKS)*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 14
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER0(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 15
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER1(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 16
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER2(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 17
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER3(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 18
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER4(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 19
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER5(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 20
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER6(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 21
        communication_struct.__init__(self, socketfd)


class ADC_BUFFER7(communication_struct):
    _fields_ = [('raw_data', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 22
        communication_struct.__init__(self, socketfd)


class PH_WORD_BUF(communication_struct):
    _fields_ = [('ph_words', c_int*CBPM_ADC_BUF_USE)]

    def __init__(self, socketfd):
        self.table_offset = 23
        communication_struct.__init__(self, socketfd)


class PROC_BUF(communication_struct):
    _fields_ = [('proc_data', PROC_DATA*CBPM_MAX_BUNCHES)]

    def __init__(self, socketfd):
        self.table_offset = 24
        communication_struct.__init__(self, socketfd)


class PROC_BUF_HEADER(communication_struct):
    _fields_ = [('species', c_int),
                ('write_ptr', c_int*CBPM_MAX_PROC_BUFS),
                ('active_buf', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 25
        communication_struct.__init__(self, socketfd)


class PROC_SUM_DAT_BUF(communication_struct):
    _fields_ = [('signal_sum', c_float*CBPM_MAX_BUNCHES),
                ('fill_count', c_int),
                ('gain_values', (c_int*CBPM_MAX_TIMING_BLOCKS)*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 26
        communication_struct.__init__(self, socketfd)


class PROC_BUF_IO(communication_struct):
    _fields_ = [('handshake', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 27
        communication_struct.__init__(self, socketfd)


class SUMM_BUF(communication_struct):
    _fields_ = [('data', SUMM_DATA*CBPM_MAX_AUTO_SAMPLES)]

    def __init__(self, socketfd):
        self.table_offset = 28
        communication_struct.__init__(self, socketfd)


class SIGNAL_STAT(communication_struct):
    _fields_ = [('signal_avg', c_float*CBPM_MAX_CARDS),
                ('signal_rms', c_float*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 29
        communication_struct.__init__(self, socketfd)


class PHASE_CONFIG(communication_struct):
    _fields_ = [('phase_jump_boundaries', (c_int*CBPM_MAX_PHASE_JUMPS)*CBI_NUM_SPECIES),
                ('phase_turn_offsets', (c_int*(CBPM_MAX_PHASE_JUMPS+1))*(CBI_NUM_SPECIES)),
                ('phase_wait_values', (c_int*(CBPM_MAX_PHASE_JUMPS+1))*(CBI_NUM_SPECIES))]

    def __init__(self, socketfd):
        self.table_offset = 30
        communication_struct.__init__(self, socketfd)


class BETA_PHASE_OUT(communication_struct):
    _fields_ = [('bunch_id', c_int),
                ('tot_turns', c_int),
                ('turn_ctr_offset', c_int),
                ('phase_results', ((((c_float*CBPM_MAX_CARDS)*CBPM_NUM_PHASE_COEFFS)*CBPM_MAX_PHASE_DIM)*CBPM_HALF_TURN_OPTIONS)*CBPM_NUM_DP_TURNS_OFFSET),
                ('signal', c_float*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 31
        communication_struct.__init__(self, socketfd)


class FIND_DELAY_OUT(communication_struct):
    _fields_ = [('max_block_delay', c_int),
                ('fcoeffs', c_float*CBPM_MAX_FIT_COEFFS),
                ('peaks', c_float*CBPM_MAX_ACQ_CONTROLLERS),
                ('offsets', c_int*CBPM_MAX_ACQ_CONTROLLERS),
                ('prevADCRMSs', c_float*CBPM_MAX_ACQ_CONTROLLERS),
                ('postADCRMSs', c_float*CBPM_MAX_ACQ_CONTROLLERS),
                ('num_retries', c_int),
                ('numTurnsToCollectPeakData', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 32
        communication_struct.__init__(self, socketfd)


class BFIND_DELAY_OUT(communication_struct):
    _fields_ = [('offsetshist', (c_int*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('peakshist', (c_float*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('chipshist', (c_int*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('blockhist', c_int*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('timingUpdateIsGoodhist', c_int*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('rollbackhist', c_int*CBPM_FIND_DELAYS_HIST_LENGTH)]

    def __init__(self, socketfd):
        self.table_offset = 33
        communication_struct.__init__(self, socketfd)


class FIND_DELAY_PARAMS(communication_struct):
    _fields_ = [('hist_index', c_int),
                ('use_data_enable', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 34
        communication_struct.__init__(self, socketfd)


class CHAN_CAL_WORK(communication_struct):
    _fields_ = [('chan_cal_data', CHAN_CAL_DATA*CBPM_MAX_CARDS)]

    def __init__(self, socketfd):
        self.table_offset = 35
        communication_struct.__init__(self, socketfd)


class PED_CAL_OUT(communication_struct):
    _fields_ = [('ped_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_CHANS_PER_CARD),
                ('ped_rms_table', ((c_float*CBPM_MAX_GAINS)*CBPM_MAX_CARDS)*CBPM_MAX_CHANS_PER_CARD)]

    def __init__(self, socketfd):
        self.table_offset = 36
        communication_struct.__init__(self, socketfd)


class RAW_PARAMS(communication_struct):
    _fields_ = [('num_turns', c_int),
                ('scale_mode', c_int),
                ('trig_turns_delay', c_int),
                ('spacex_turn', c_int),
                ('use_data_enable', c_int),
                ('trig_mask', c_int),
                ('phase_race_wait', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 37
        communication_struct.__init__(self, socketfd)


class PROC_PARAMS(communication_struct):
    _fields_ = [('avg_mode', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 38
        communication_struct.__init__(self, socketfd)


class CAL_PARAMS(communication_struct):
    _fields_ = [('delay_cal', c_int),
                ('gain_cal', c_int),
                ('delay_init', c_int),
                ('gain_xcal', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 39
        communication_struct.__init__(self, socketfd)


class DIAGNOSTIC(communication_struct):
    _fields_ = [('pre_pf_peak_block_delays', c_int*CBPM_MAX_ACQ_CONTROLLERS),
                ('pre_pf_offset_chan_delays', c_int*CBPM_MAX_ACQ_CONTROLLERS),
                ('scrub_value', c_int),
                ('sample_at_zero_crossing', c_int),
                ('magic_wait_calibration_value', c_int),
                ('test_step_index', c_int)]

    def __init__(self, socketfd):
        self.table_offset = 40
        communication_struct.__init__(self, socketfd)


class CODE_PARAMS(communication_struct):
    _fields_ = [('tests', TEST_PARAMS_STRUCT*CBPM_NUM_TESTS),
                ('execution_flags', c_int*CBPM_MAX_NUM_EXECUTION_FLAGS)]

    def __init__(self, socketfd):
        self.table_offset = 41
        communication_struct.__init__(self, socketfd)


class TEST_RESULTS(communication_struct):
    _fields_ = [('EncodedStatus', c_int*CBPM_NUM_TESTS_ENCODED),
                ('Statuses', (c_int*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_NUM_TESTS)]

    def __init__(self, socketfd):
        self.table_offset = 42
        communication_struct.__init__(self, socketfd)


class BTEST_RESULTS(communication_struct):
    _fields_ = [('Statuseshist', ((c_int*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_NUM_TESTS)*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('StatusVals', ((c_float*CBPM_MAX_ACQ_CONTROLLERS)*CBPM_NUM_TESTS)*CBPM_FIND_DELAYS_HIST_LENGTH),
                ('statushist', c_int*CBPM_FIND_DELAYS_HIST_LENGTH)]

    def __init__(self, socketfd):
        self.table_offset = 43
        communication_struct.__init__(self, socketfd)


class BPM(instrument):
    """Defines a BPM instrument.

    Contains core and BPM-specific communication data structures."""
    def __init__(self, host):
        instrument.__init__(self, host)
        self.cmd_params = CMD_PARAMS(self.socketfd)
        self.temperatures = TEMPERATURES(self.socketfd)
        self.timing_config = TIMING_CONFIG(self.socketfd)
        self.gain_config = GAIN_CONFIG(self.socketfd)
        self.pedestal_config = PEDESTAL_CONFIG(self.socketfd)
        self.op_timing = OP_TIMING(self.socketfd)
        self.op_gain = OP_GAIN(self.socketfd)
        self.raw_data_header = RAW_DATA_HEADER(self.socketfd)
        self.adc_buffer0 = ADC_BUFFER0(self.socketfd)
        self.adc_buffer1 = ADC_BUFFER1(self.socketfd)
        self.adc_buffer2 = ADC_BUFFER2(self.socketfd)
        self.adc_buffer3 = ADC_BUFFER3(self.socketfd)
        self.adc_buffer4 = ADC_BUFFER4(self.socketfd)
        self.adc_buffer5 = ADC_BUFFER5(self.socketfd)
        self.adc_buffer6 = ADC_BUFFER6(self.socketfd)
        self.adc_buffer7 = ADC_BUFFER7(self.socketfd)
        self.ph_word_buf = PH_WORD_BUF(self.socketfd)
        self.proc_buf = PROC_BUF(self.socketfd)
        self.proc_buf_header = PROC_BUF_HEADER(self.socketfd)
        self.proc_sum_dat_buf = PROC_SUM_DAT_BUF(self.socketfd)
        self.proc_buf_io = PROC_BUF_IO(self.socketfd)
        self.summ_buf = SUMM_BUF(self.socketfd)
        self.signal_stat = SIGNAL_STAT(self.socketfd)
        self.phase_config = PHASE_CONFIG(self.socketfd)
        self.beta_phase_out = BETA_PHASE_OUT(self.socketfd)
        self.find_delay_out = FIND_DELAY_OUT(self.socketfd)
        self.bfind_delay_out = BFIND_DELAY_OUT(self.socketfd)
        self.find_delay_params = FIND_DELAY_PARAMS(self.socketfd)
        self.chan_cal_work = CHAN_CAL_WORK(self.socketfd)
        self.ped_cal_out = PED_CAL_OUT(self.socketfd)
        self.raw_params = RAW_PARAMS(self.socketfd)
        self.proc_params = PROC_PARAMS(self.socketfd)
        self.cal_params = CAL_PARAMS(self.socketfd)
        self.diagnostic = DIAGNOSTIC(self.socketfd)
        self.code_params = CODE_PARAMS(self.socketfd)
        self.test_results = TEST_RESULTS(self.socketfd)
        self.btest_results = BTEST_RESULTS(self.socketfd)
