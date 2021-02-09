#
# file_io.py
#
#-*- python -*-
#

from ctypes import *
from os import environ

libdir = environ['ACC_RELEASE_DIR']+'/production/lib'

cbpmfio = CDLL(libdir+'/libcbpmfio.so')

CBPMFIO_MAX_FIELD_ADDRESSES = 10


def open_data_file(full_filename):

    filename_b = str.encode(full_filename)
    cbpmfio.cbpmfio_open_file(filename_b)




# def write_file_header(values):

#     fio_addrs_type = c_long * CBPMFIO_MAX_FIELD_ADDRESSES
#     fio_addrs = fio_addrs_type()
    
#     for idx, value in enumerate(values):
#         fio_addrs

    



def write_cesr_header():

    condx = c_int()
    cern_raw = c_int()
    cern_curr = c_float()

    fio_addrs_type = c_long * CBPMFIO_MAX_FIELD_ADDRESSES
    fio_addrs = fio_addrs_type()
    
    fio_addrs[0] = addressof(condx)
    cbpmfio.cbpmfio_map_RDv3_cesr_field(0, byref(fio_addrs))

    fio_addrs[0] = addressof(cern_raw)
    cbpmfio.cbpmfio_map_RDv3_cesr_field(1, byref(fio_addrs))

    fio_addrs[0] = addressof(cern_curr)
    cbpmfio.cbpmfio_map_RDv3_cesr_field(2, byref(fio_addrs))

    condx.value = 666
    cern_raw.value = 777
    cern_curr.value = 123.456

    cbpmfio.cbpmfio_write_cesr_header()


#def write_instrument_header(values):


def write_data_fields(tblock_v, pword_v, TI_v, BI_v, BO_v, TO_v):

    tblock = c_int()
    pword = c_int()
    TI = c_int()
    BI = c_int()
    BO = c_int()
    TO = c_int()

    tblock.value = tblock_v
    pword.value = pword_v
    TI.value = TI_v
    BI.value = BI_v
    BO.value = BO_v
    TO.value = TO_v

    fio_addrs_type = c_long * CBPMFIO_MAX_FIELD_ADDRESSES
    fio_addrs = fio_addrs_type()

    fio_addrs[0] = addressof(tblock)
    fio_addrs[1] = addressof(pword)
    fio_addrs[2] = addressof(TI)
    fio_addrs[3] = addressof(BI)
    fio_addrs[4] = addressof(BO)
    fio_addrs[5] = addressof(TO)
    cbpmfio.cbpmfio_map_RDv3_data_fields(byref(fio_addrs))

    cbpmfio.cbpmfio_write_data_fields()

        

def close_data_file():

    cbpmfio.cbpmfio_close_file()
