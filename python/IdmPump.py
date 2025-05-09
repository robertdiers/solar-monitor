#!/usr/bin/env python

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


# -----------------------------------------
# Routine to read a float
def readfloat(client, myadr_dec, unitid):
    r1 = client.read_holding_registers(myadr_dec, count=2, slave=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    result_FloatRegister = round(FloatRegister.decode_32bit_float(), 2)
    # the new code is giving strange values...
    # FloatRegister = client.convert_from_registers(r1.registers, ModbusTcpClient.DATATYPE.FLOAT32, Endian.LITTLE)
    # result_FloatRegister = round(FloatRegister,2)
    return result_FloatRegister


def read(idm_ip, idm_port):
    try:

        # connection iDM
        client = ModbusTcpClient(idm_ip, port=idm_port)
        client.connect()

        # solar power stored in 74
        return readfloat(client, 74, 1)

    except Exception as ex:
        print("ERROR IDM: ", ex)
    finally:
        client.close()
