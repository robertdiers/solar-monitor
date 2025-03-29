#!/usr/bin/env python

import time
import math

import Config
import Daly
import TimescaleDb

# {'Device_Name': 'DALY2', 'Device_IP': '192.168.50.81', 'Device_ESP_VCC': 2.64, 'Device_Relais_Active': False,
# 'Device_Relais_Manual': False, 'Pack_Voltage': 53.8, 'Pack_Current': 1.1, 'Pack_Power': 59.18, 'Pack_SOC': 100,
# 'Pack_Remaining_mAh': 90000, 'Pack_Cycles': 60, 'Pack_BMS_Temp': 19, 'Pack_Cell_Temp': 19, 'Pack_High_CellNr': 14,
# 'Pack_High_CellV': 3.397, 'Pack_Low_CellNr': 9, 'Pack_Low_CellV': 3.34, 'Pack_Cell_Diff': 57,
# 'Pack_DischargeFET': True, 'Pack_ChargeFET': True, 'Pack_Status': 'Charge', 'Pack_Cells': 16, 'Pack_Heartbeat': 71,
# 'Pack_Balance_Active': False, 'CellV_CellV_1': 3.369, 'CellV_Balance_1': False, 'CellV_CellV_2': 3.36,
# 'CellV_Balance_2': False, 'CellV_CellV_3': 3.375, 'CellV_Balance_3': False, 'CellV_CellV_4': 3.358,
# 'CellV_Balance_4': False, 'CellV_CellV_5': 3.362, 'CellV_Balance_5': False, 'CellV_CellV_6': 3.36,
# 'CellV_Balance_6': False, 'CellV_CellV_7': 3.346, 'CellV_Balance_7': False, 'CellV_CellV_8': 3.35,
# 'CellV_Balance_8': False, 'CellV_CellV_9': 3.34, 'CellV_Balance_9': False, 'CellV_CellV_10': 3.391,
# 'CellV_Balance_10': False, 'CellV_CellV_11': 3.346, 'CellV_Balance_11': False, 'CellV_CellV_12': 3.348,
# 'CellV_Balance_12': False, 'CellV_CellV_13': 3.392, 'CellV_Balance_13': False, 'CellV_CellV_14': 3.394,
# 'CellV_Balance_14': False, 'CellV_CellV_15': 3.391, 'CellV_Balance_15': False, 'CellV_CellV_16': 3.386,
# 'CellV_Balance_16': False, 'CellTemp_Cell_Temp_1': 19}

# define interesting attributes
attributes = ["Pack_Voltage", "Pack_Power", "Pack_SOC", "Pack_Cycles", "Pack_High_CellV", "Pack_Low_CellV",
              "Pack_Cell_Diff", "Pack_Cell_Temp", "Pack_BMS_Temp"]
# max 48 blocks
for x in range(17):
    attributes.append("CellV_CellV_"+str(x))


def writedb(name, json):
    # print (json)
    global attributes
    for attribute in attributes:
        # print(attribute)
        if attribute in json:
            # print(attribute+": "+str(json[attribute]))
            value = 0
            if math.isnan(json[attribute]):
                print(attribute+" nan: "+str(json[attribute]))
            else:
                value = float(json[attribute])
                if attribute in 'Pack_Cell_Diff':
                    value = value / 1000.0
                    # print (value)
                    TimescaleDb.writeV(name+'_'+attribute, value)
                if attribute in 'Pack_SOC':
                    value = value / 100.0
                    # print (value)
                    TimescaleDb.writeP(name+'_'+attribute, value)
                if attribute in 'Pack_Voltage':
                    TimescaleDb.writeV(name+'_'+attribute, value)
                if attribute in 'Pack_Power':
                    TimescaleDb.writeW(name+'_'+attribute, value)
                if attribute in 'Pack_Cycles':
                    TimescaleDb.writeK(name+'_'+attribute, value)
                if attribute in 'Pack_High_CellV':
                    TimescaleDb.writeV(name+'_'+attribute, value)
                if attribute in 'Pack_Low_CellV':
                    TimescaleDb.writeV(name+'_'+attribute, value)
                if attribute in 'Pack_Cell_Temp':
                    TimescaleDb.writeT(name+'_'+attribute, value)
                if attribute in 'Pack_BMS_Temp':
                    TimescaleDb.writeT(name+'_'+attribute, value)
                if attribute.startswith('CellV_CellV'):
                    TimescaleDb.writeV(name+'_'+attribute, value)


if __name__ == "__main__":
    daly1 = ''
    daly2 = ''
    daly3 = ''
    conf = Config.read()
    try:

        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])

        # subscribe all Daly
        daly1 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                               conf["daly1_mqtt_name"], writedb, "Daly1")
        daly2 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                               conf["daly2_mqtt_name"], writedb, "Daly2")
        daly3 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                               conf["daly3_mqtt_name"], writedb, "Daly3")

        # run 10 minutes
        minutes = 0
        while (minutes < 10):
            time.sleep(60)
            minutes = minutes + 1
            # print ("waiting")

    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        TimescaleDb.close()
        Daly.close(daly1, conf["daly1_mqtt_name"])
        Daly.close(daly2, conf["daly2_mqtt_name"])
        Daly.close(daly3, conf["daly3_mqtt_name"])
