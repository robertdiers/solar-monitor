#!/usr/bin/env python

from datetime import datetime
import time
import math

import Config
import Daly
import TimescaleDb

#{"Pack":{"Device_Name":"DALY1","Device_IP":"192.168.1.29","Voltage":51.5,"Current":5.6,"Power":288.4,"SOC":48.5,"Remaining_mAh":43650,"Cycles":79,
#"BMS_Temp":13,"Cell_Temp":13,"High_CellNr":15,"High_CellV":3.249,"Low_CellNr":9,"Low_CellV":3.189,"Cell_Diff":60,"DischargeFET":true,"ChargeFET":true,"Status":"Charge","Cells":16,"Heartbeat":85,"Balance_Active":false,"Relais_Active":false,"Relais_Manual":false},
#"CellV":{"CellV 1":3.244,"Balance 1":false,"CellV 2":3.227,"Balance 2":false,"CellV 3":3.232,"Balance 3":false,"CellV 4":3.199,"Balance 4":false,"CellV 5":3.204,"Balance 5":false,"CellV 6":3.191,"Balance 6":false,"CellV 7":3.229,"Balance 7":false,"CellV 8":3.209,"Balance 8":false,"CellV 9":3.188,"Balance 9":false,"CellV 10":3.189,"Balance 10":false,"CellV 11":3.21,"Balance 11":false,"CellV 12":3.207,"Balance 12":false,"CellV 13":3.249,"Balance 13":false,"CellV 14":3.249,"Balance 14":false,"CellV 15":3.249,"Balance 15":false,"CellV 16":3.239,"Balance 16":false},"CellTemp":{"Cell_Temp1":13}}

#define interesting attributes        
attributes = ["Pack_Voltage", "Pack_Power", "Pack_SOC", "Pack_Cycles", "Pack_High_CellV", "Pack_Low_CellV", "Pack_Cell_Diff", "Pack_Cell_Temp", "Pack_BMS_Temp"]
#max 48 blocks
for x in range(16):
    attributes.append("CellV_CellV "+str(x))

def writedb(name, json):
    print (json)
    global attributes
    for attribute in attributes:
        #print(attribute)
        if attribute in json:
            #print(attribute+": "+str(json[attribute]))
            value = 0
            if math.isnan(json[attribute]):
                print(attribute+" nan: "+str(json[attribute]))
            else:
                value = float(json[attribute])
                if attribute in 'Pack_Cell_Diff':
                    value = value / 1000.0
                    #print (value)
                    TimescaleDb.writeV(name+'_'+attribute, value)
                if attribute in 'Pack_SOC':
                    value = value / 100.0
                    #print (value)
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
        
        #subscribe all Daly
        daly1 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"], conf["daly1_mqtt_name"], writedb, "Daly1")
        daly2 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"], conf["daly2_mqtt_name"], writedb, "Daly2")
        daly3 = Daly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"], conf["daly3_mqtt_name"], writedb, "Daly3")

        #run 10 minutes
        minutes = 0
        while (minutes < 10):
            time.sleep(60)
            minutes = minutes + 1
            #print ("waiting")

    except Exception as ex:
        print ("ERROR: ", ex) 
    finally:
        TimescaleDb.close()
        Daly.close(daly1, conf["daly1_mqtt_name"])
        Daly.close(daly2, conf["daly2_mqtt_name"])
        Daly.close(daly3, conf["daly3_mqtt_name"])
