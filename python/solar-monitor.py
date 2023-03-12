#!/usr/bin/env python

from datetime import datetime
import math

import TimescaleDb
import Tasmota
import BYD
import Config
import Kostal
import IdmPump
import Solax
import Goodwe

# metrics from Tasmota
def tasmota(temp_mqtt_name, goodwe_mqtt_name):
    try:
        result = Tasmota.get(temp_mqtt_name, "8", ["StatusSNS_SI7021_Temperature"])
        if math.isnan(result["StatusSNS_SI7021_Temperature"]):
            print(attribute+" nan: "+str(result["StatusSNS_SI7021_Temperature"]))
        else:
            TimescaleDb.writeT('tech_room', result["StatusSNS_SI7021_Temperature"])
    except Exception as ex:
        print ("ERROR tasmota "+temp_mqtt_name+": ", ex)
    try:
        result = Tasmota.get(goodwe_mqtt_name, "8", ["StatusSNS_ENERGY_Power", "StatusSNS_ENERGY_Today"])
        TimescaleDb.writeW('goodwe_tasmota_power', result["StatusSNS_ENERGY_Power"])
        TimescaleDb.writeK('goodwe_tasmota_dailyyield', result["StatusSNS_ENERGY_Today"])
    except Exception as ex:
        print ("ERROR tasmota "+goodwe_mqtt_name+": ", ex)  

# metrics from BYD
def byd(byd_ip, byd_port):
    try:
        bydvalues = BYD.read(byd_ip, byd_port)
        TimescaleDb.writeP('byd_soc', round(bydvalues["soc"]/100, 2))
        TimescaleDb.writeV('byd_maxvolt', bydvalues["maxvolt"])
        TimescaleDb.writeV('byd_minvolt', bydvalues["minvolt"])
        TimescaleDb.writeP('byd_soh', round(bydvalues["soh"]/100, 2))
        TimescaleDb.writeT('byd_maxtemp', bydvalues["maxtemp"])
        TimescaleDb.writeT('byd_mintemp', bydvalues["mintemp"])
        TimescaleDb.writeT('byd_battemp', bydvalues["battemp"])
        #TimescaleDb.write('byd_error', bydvalues["error"])
        TimescaleDb.writeW('byd_power', bydvalues["power"])
        TimescaleDb.writeV('byd_diffvolt', bydvalues["diffvolt"])
    except Exception as ex:
        print ("ERROR byd: ", ex)  

# metrics from IDM
def idm(idm_ip, idm_port):
    try:
        TimescaleDb.writeW('idm_solar', IdmPump.read(idm_ip, idm_port)*1000)
    except Exception as ex:
        print ("ERROR idm: ", ex)

# metrics from Kostal
def kostal(inverter_ip, inverter_port):
    try:
        #read Kostal
        kostalvalues = Kostal.read(inverter_ip, inverter_port)
        TimescaleDb.writeW('kostal_consumption', kostalvalues["consumption_total"])
        TimescaleDb.writeW('kostal_inverter', kostalvalues["inverter"])
        TimescaleDb.writeW('kostal_powertobattery', kostalvalues["powerToBattery"])
        TimescaleDb.writeP('kostal_batterypercent', (kostalvalues["batterypercent"]/100))
        TimescaleDb.writeW('kostal_generation', kostalvalues["generation"]) 
        TimescaleDb.writeW('kostal_powertogrid', kostalvalues["powerToGrid"])
        TimescaleDb.writeW('kostal_surplus', kostalvalues["surplus"])
        TimescaleDb.writeK('kostal_dailyyield', kostalvalues["dailyyield"])
    except Exception as ex:
        print ("ERROR kostal: ", ex)

# metrics from Solax
def solax(solax_tokenid, solax_inverter):
    try:
        #read Solax
        invert = solax_inverter.split(",")
        #print(invert)
        for i in invert:
            res = Solax.read(solax_tokenid, i)
            #print(res)
            sn = res["sn"]
            TimescaleDb.writeW('solax_power_'+sn, res["acpower"])
            TimescaleDb.writeK('solax_yieldtoday_'+sn, res["yieldtoday"])
            #TimescaleDb.writeW('solax_feedinpower_'+sn, res["feedinpower"])
            #TimescaleDb.writeK('solax_feedinenergy_'+sn, res["feedinenergy"])
    except Exception as ex:
        print ("ERROR solax: ", ex)

# metrics from Goodwe
def goodwe(sems_user, sems_password, sems_stationid):
    try:
        #read Goodwe
        res = Goodwe.read(sems_user, sems_password, sems_stationid)
        print(res)
    except Exception as ex:
        print ("ERROR goodwe: ", ex)

if __name__ == "__main__":  
    #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()
        
        #connect interfaces
        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])
        Tasmota.connect(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"])

        #metrics
        tasmota(conf["temp_mqtt_name"], conf["goodwe_mqtt_name"])
        byd(conf["byd_ip"], conf["byd_port"])
        idm(conf["idm_ip"], conf["idm_port"])
        kostal(conf["inverter_ip"], conf["inverter_port"])
        solax(conf["solax_tokenid"], conf["solax_inverter"])
        #goodwe(conf["sems_user"], conf["sems_password"], conf["sems_stationid"])

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " OK")  

        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR: ", ex) 
    finally:
        TimescaleDb.close()     