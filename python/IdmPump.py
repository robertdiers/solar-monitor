#!/usr/bin/env python

import pymodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

#-----------------------------------------
# Routine to read a float    
def readfloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,slave=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)   

def read(idm_ip, idm_port):  
    try:
        
        #connection iDM
        client = ModbusTcpClient(idm_ip,port=idm_port)     
        client.connect()  

        #solar power stored in 74
        return readfloat(client,74,1)
  
    except Exception as ex:
        print ("ERROR IDM: ", ex)
    finally:
        client.close() 
