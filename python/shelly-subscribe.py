#!/usr/bin/env python

import time
import math

import Config
import Shelly
import TimescaleDb

# {
#   "id": 0,
#   "voltage": 245.2,
#   "current": 4.74,
#   "apower": -1166.5,
#   "freq": 50,
#   "aenergy": {
#     "total": 8598.783,
#     "by_minute": [
#       19479.399,
#       19262.962,
#       19479.399,
#     ],
#     "minute_ts": 1743941939
#   },
#   "ret_aenergy": {
#     "total": 8602.246,
#     "by_minute": [
#       19479.399,
#       19262.962,
#       19479.399,
#     ],
#     "minute_ts": 1743941939
#   }
# }

# define interesting attributes, aenergy simply counts up - need to substract yesterdays value
attributes = ["apower", "aenergy_total"]


def writedb(name, json):
    # print(json)
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
                if attribute in 'apower':
                    value = -value
                    # print(attribute+" apower: "+str(value))
                    TimescaleDb.writeW(name, value)
                if attribute in 'aenergy_total':
                    # this is a kind of a counter, not a per-day-value
                    # we need to fill a counter table and substract yesterdays value
                    key = name
                    # wh to kwh
                    today_counter = value / 1000
                    # print(attribute+": "+str(today_counter))
                    # 1. update counter table (will update the counter for 'today')
                    TimescaleDb.writeKTC(key, today_counter)
                    # 2. get counter value from yesterday
                    yesterday_counter = TimescaleDb.readKTCYesterday(key)
                    # print(attribute+" yesterday: "+str(yesterday_counter))
                    # 3. check if this is a resetted counter
                    if yesterday_counter > today_counter:
                        print('detected resetted counter - ignoring yesterdays kwh')
                        yesterday_counter = 0
                    # 4. calculate the diff
                    today_kwh = today_counter - yesterday_counter
                    # print(attribute+" today_kwh: "+str(today_kwh))
                    # 5. store todays value
                    TimescaleDb.writeK(key, today_kwh)
                    TimescaleDb.writeKT(key, today_kwh)


if __name__ == "__main__":
    shelly1 = ''
    shelly2 = ''
    shelly3 = ''
    shelly4 = ''
    shelly5 = ''
    shelly6 = ''
    shelly7 = ''
    shelly8 = ''
    conf = Config.read()
    try:

        TimescaleDb.connect(conf["timescaledb_ip"], conf["timescaledb_username"], conf["timescaledb_password"])

        # subscribe all Shelly
        shelly1 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly1_mqtt_name"], writedb, "shelly1")
        shelly2 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly2_mqtt_name"], writedb, "shelly2")
        shelly3 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly3_mqtt_name"], writedb, "shelly3")
        shelly4 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly4_mqtt_name"], writedb, "shelly4")
        shelly5 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly5_mqtt_name"], writedb, "shelly5")
        shelly6 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly6_mqtt_name"], writedb, "shelly6")
        shelly7 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly7_mqtt_name"], writedb, "shelly7")
        shelly8 = Shelly.subscribe(conf["mqtt_broker"], conf["mqtt_port"], conf["mqtt_user"], conf["mqtt_password"],
                                   conf["shelly8_mqtt_name"], writedb, "shelly8")

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
        Shelly.close(shelly1, conf["shelly1_mqtt_name"])
        Shelly.close(shelly2, conf["shelly2_mqtt_name"])
        Shelly.close(shelly3, conf["shelly3_mqtt_name"])
        Shelly.close(shelly4, conf["shelly4_mqtt_name"])
        Shelly.close(shelly5, conf["shelly5_mqtt_name"])
        Shelly.close(shelly6, conf["shelly6_mqtt_name"])
        Shelly.close(shelly7, conf["shelly7_mqtt_name"])
        Shelly.close(shelly8, conf["shelly8_mqtt_name"])
