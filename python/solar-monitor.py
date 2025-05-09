#!/usr/bin/env python

from datetime import datetime
import asyncio
import math

import TimescaleDb
import Tasmota
import BYD
import Config
import Kostal
import IdmPump
# import Solax
# import Goodwe
import Goodwe_Local


# temp metrics from Tasmota
def tasmota_temp(mqtt_name, alias):
    try:
        result = Tasmota.get(mqtt_name, "8", ["StatusSNS_DS18B20_Temperature"])
        if math.isnan(result["StatusSNS_DS18B20_Temperature"]):
            print("StatusSNS_DS18B20_Temperature nan: "+str(result["StatusSNS_DS18B20_Temperature"]))
        else:
            TimescaleDb.writeT('bath_room', result["StatusSNS_DS18B20_Temperature"])
    except Exception as ex:
        print("ERROR tasmota " + mqtt_name + ": ", ex)


# power meter metrcis from Tasmota
def tasmota_pm(mqtt_name, alias):
    try:
        result = Tasmota.get(mqtt_name, "8", ["StatusSNS_ENERGY_Power", "StatusSNS_ENERGY_Today"])
        if math.isnan(result["StatusSNS_ENERGY_Power"]):
            print("StatusSNS_ENERGY_Power nan: "+str(result["StatusSNS_ENERGY_Power"]))
        else:
            TimescaleDb.writeW(alias + '_power', result["StatusSNS_ENERGY_Power"])
        if math.isnan(result["StatusSNS_ENERGY_Today"]):
            print("StatusSNS_ENERGY_Today nan: "+str(result["StatusSNS_ENERGY_Today"]))
        else:
            TimescaleDb.writeK(alias, result["StatusSNS_ENERGY_Today"])
            # write to total table
            TimescaleDb.writeKT(alias, result["StatusSNS_ENERGY_Today"])
    except Exception as ex:
        print("ERROR tasmota " + mqtt_name + ": ", ex)


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
        # TimescaleDb.write('byd_error', bydvalues["error"])
        TimescaleDb.writeW('byd_power', bydvalues["power"])
        TimescaleDb.writeV('byd_diffvolt', bydvalues["diffvolt"])
    except Exception as ex:
        print("ERROR byd: ", ex)


# metrics from IDM
def idm(idm_ip, idm_port):
    try:
        TimescaleDb.writeW('idm_solar', IdmPump.read(idm_ip, idm_port)*1000)
    except Exception as ex:
        print("ERROR idm: ", ex)


# metrics from Kostal
def kostal(inverter_ip, inverter_port):
    try:
        # read Kostal
        kostalvalues = Kostal.read(inverter_ip, inverter_port)

        # do not log all values between 23 and 3 o'clock
        store_all = False
        if datetime.now().hour < 23 and datetime.now().hour >= 3:
            store_all = True

        # write to db
        TimescaleDb.writeW('kostal_consumption', kostalvalues["consumption_total"])
        TimescaleDb.writeW('kostal_inverter', kostalvalues["inverter"])
        TimescaleDb.writeW('kostal_powertobattery', kostalvalues["powerToBattery"])
        TimescaleDb.writeP('kostal_batterypercent', (kostalvalues["batterypercent"]/100))
        TimescaleDb.writeW('kostal_powertogrid', kostalvalues["powerToGrid"])
        TimescaleDb.writeW('kostal_surplus', kostalvalues["surplus"])

        if store_all:
            TimescaleDb.writeW('kostal_generation', kostalvalues["generation"])
            TimescaleDb.writeK('kostal', kostalvalues["dailyyield"])
            # update latest daily yield
            TimescaleDb.writeKT('kostal', kostalvalues["dailyyield"])

    except Exception as ex:
        print("ERROR kostal: ", ex)


# # metrics from Solax
# def solax(solax_tokenid, solax_inverter):
#     try:
#         # read Solax
#         invert = solax_inverter.split(",")
#         # print(invert)
#         for i in invert:
#             res = Solax.read(solax_tokenid, i)
#             # print(res)
#             sn = res["sn"]
#             TimescaleDb.writeW('solax_power_'+sn, res["acpower"])
#             TimescaleDb.writeK('solax_yieldtoday_'+sn, res["yieldtoday"])
#             # TimescaleDb.writeW('solax_feedinpower_'+sn, res["feedinpower"])
#             # TimescaleDb.writeK('solax_feedinenergy_'+sn, res["feedinenergy"])
#     except Exception as ex:
#         print("ERROR solax: ", ex)


# # metrics from Goodwe
# def goodwe(sems_user, sems_password, sems_stationid):
#     try:
#         # read Goodwe
#         res = Goodwe.read(sems_user, sems_password, sems_stationid)
#         # print(res)
#         TimescaleDb.writeT('goodwe_temp', res["tempperature"])

#         # 53.1V/0.7A/37W
#         battery = res["battery"].split('/')
#         # print(battery)
#         TimescaleDb.writeV('goodwe_battery_volt', float(battery[0].replace('V', '')))
#         TimescaleDb.writeW('goodwe_battery_watt', float(battery[2].replace('W', '')))

#         # print('1')
#         TimescaleDb.writeP('goodwe_battery_soh', round(float(res["soh"].replace('%', ''))/100, 2))
#         TimescaleDb.writeP('goodwe_battery_soc', round(float(res["soc"].replace('%', ''))/100, 2))

#         # print('2')
#         # print(res["output_power"].replace('W',''))
#         TimescaleDb.writeW('goodwe_output', res["output_power"].replace('W', ''))
#         # print('3')
#         TimescaleDb.writeK('goodwe_yieldtoday', res["daily_generation"].replace('kWh', ''))

#         # 330.9V/0.4A
#         # print('4')
#         pv1 = res["pv_input_1"].split('/')
#         pv2 = res["pv_input_2"].split('/')
#         # print(pv1)
#         # print(pv2)
#         pv1w = float(pv1[0].replace('V', '')) * float(pv1[1].replace('A', ''))
#         pv2w = float(pv2[0].replace('V', '')) * float(pv2[1].replace('A', ''))
#         # print(pv1w)
#         # print(pv2w)
#         TimescaleDb.writeW('goodwe_pv', round(pv1w + pv2w, 2))

#     except Exception as ex:
#         print("ERROR goodwe: ", ex)


# # metrics from Goodwe
def goodwe_local(goodwe_ip):
    try:
        # read Goodwe
        asyncio.run(Goodwe_Local.Goodwe.get_runtime_data(goodwe_ip))
    except Exception as ex:
        print("ERROR goodwe: ", ex)


if __name__ == "__main__":
    # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        conf = Config.read()

        # connect interfaces
        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])
        Tasmota.connect(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"])

        # metrics
        tasmota_temp(conf["temp_mqtt_name"], 'bath_room')
        # tasmota_pm(conf["goodwe_mqtt_name"], 'goodwe_tasmota')
        byd(conf["byd_ip"], conf["byd_port"])
        idm(conf["idm_ip"], conf["idm_port"])
        kostal(conf["inverter_ip"], conf["inverter_port"])
        goodwe_local(conf["goodwe_ip"])

        # deactivated cloud solutions
        # solax(conf["solax_tokenid"], conf["solax_inverter"])
        # goodwe(conf["sems_user"], conf["sems_password"], conf["sems_stationid"])

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " OK")

        # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")

    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        TimescaleDb.close()
