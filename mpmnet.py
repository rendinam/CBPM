#
# Python wrappers for selected mpmnet library functions
#

from ctypes import *
from os import environ

# Locate and load the mpmnet.so library for CESR MPM communications.
libdir = environ['ACC_RELEASE_DIR']+'/production/lib'
mpmnet = CDLL(libdir+'/libmpmnet.so')

def connect(client_type):

    client_type_b = str.encode(client_type)
    mpmnet.Mnet_connect(client_type_b)



def disconnect():

    mpmnet.Mnet_disconnect()



def vxgetn(node, start_element, end_element):

    node_b = str.encode(node)

    values = []
    numvals = end_element - start_element
    if numvals == 0:
        numvals = 1
    elif numvals < 0:
        raise IndexError
    
    raw_values = (c_int * numvals)()

    mpmnet.vxgetn_c(node_b, start_element, end_element, byref(raw_values))
    
    for val in raw_values:
        values.append(val)

    return values
        


def vxputn(node, start_element, end_element, data):

    node_b = str.encode(node)

    numvals = end_element - start_element
    if numvals == 0:
        numvals = 1
    elif numvals < 0:
        raise IndexError

    raw_values = (c_int * numvals)()

    for idx, val in enumerate(data):
        raw_values[idx] = val

    mpmnet.vxputn_c(node_b, start_element, end_element, byref(raw_values))
    
