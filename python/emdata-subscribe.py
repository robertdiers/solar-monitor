#!/usr/bin/env python

import math
import threading

import Config
import Shelly
import TimescaleDb

# cumulative Shelly Pro 3EM counters (already in kWh) and their database keys
counters = {
    "total_act": "shellypro3em_energy_import",
    "total_act_ret": "shellypro3em_energy_export",
}

done = threading.Event()
written = False


def writedb(name, json):
    global written
    if written:
        return
    written = True
    try:
        for attribute, key in counters.items():
            value = json.get(attribute)
            if value is None or math.isnan(value):
                continue
            # 1. update the counter table (value for 'today')
            today_counter = float(value)
            TimescaleDb.writeKTC(key, today_counter)
            # 2. get the counter value from yesterday
            yesterday_counter = TimescaleDb.readKTCYesterday(key)
            # 3. check if this is a resetted counter
            if yesterday_counter > today_counter:
                print('detected resetted counter - ignoring yesterdays kwh')
                yesterday_counter = 0
            # 4. calculate the diff
            today_kwh = today_counter - yesterday_counter
            # 5. store today's value
            TimescaleDb.writeK(key, today_kwh)
            TimescaleDb.writeKT(key, today_kwh)
    except Exception as ex:
        print("ERROR emdata: ", ex)
    finally:
        done.set()


if __name__ == "__main__":
    client = None
    conf = Config.read()
    try:
        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"],
                            conf["timescaledb_password"])

        client = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"],
                                  conf["mqtt_user"], conf["mqtt_password"],
                                  conf["emdata_mqtt_name"], writedb, "pro3em_energy")
        if client is None:
            print("ERROR emdata: no MQTT client")
        else:
            # emdata:0 is published about every 60 seconds
            done.wait(75)
            if not done.is_set():
                print("ERROR emdata: timeout waiting for message")
    except Exception as ex:
        print("ERROR: ", ex)
    finally:
        if client is not None:
            Shelly.close(client, conf["emdata_mqtt_name"])
            client.disconnect()
        TimescaleDb.close()
