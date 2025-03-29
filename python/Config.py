#!/usr/bin/env python

import configparser
import os

# read config
config = configparser.ConfigParser()


def read():
    try:
        # read config
        # config.read('solar-monitor-rdiers.ini')
        config.read('solar-monitor.ini')

        values = {}

        # read config and default values
        values["byd_ip"] = config['BydSection']['byd_ip']
        values["byd_port"] = int(config['BydSection']['byd_port'])
        if os.getenv('BYD_IP', 'None') != 'None':
            values["byd_ip"] = os.getenv('BYD_IP')
            # print ("using env: BYD_IP")
        if os.getenv('BYD_PORT', 'None') != 'None':
            values["byd_port"] = int(os.getenv('BYD_PORT'))
            # print ("using env: BYD_PORT")

        values["temp_mqtt_name"] = config['MqttTopicSection']['temp_mqtt_name']
        values["goodwe_mqtt_name"] = config['MqttTopicSection']['goodwe_mqtt_name']
        values["daly1_mqtt_name"] = config['MqttTopicSection']['daly1_mqtt_name']
        values["daly2_mqtt_name"] = config['MqttTopicSection']['daly2_mqtt_name']
        values["daly3_mqtt_name"] = config['MqttTopicSection']['daly3_mqtt_name']
        if os.getenv('TEMP_MQTT_NAME', 'None') != 'None':
            values["temp_mqtt_name"] = os.getenv('TEMP_MQTT_NAME')
            # print ("using env: TEMP_MQTT_NAME")
        if os.getenv('GOODWE_MQTT_NAME', 'None') != 'None':
            values["goodwe_mqtt_name"] = os.getenv('GOODWE_MQTT_NAME')
            # print ("using env: GOODWE_MQTT_NAME")
        if os.getenv('DALY1_MQTT_NAME', 'None') != 'None':
            values["daly1_mqtt_name"] = os.getenv('DALY1_MQTT_NAME')
            # print ("using env: DALY1_MQTT_NAME")
        if os.getenv('DALY2_MQTT_NAME', 'None') != 'None':
            values["daly2_mqtt_name"] = os.getenv('DALY2_MQTT_NAME')
            # print ("using env: DALY2_MQTT_NAME")
        if os.getenv('DALY3_MQTT_NAME', 'None') != 'None':
            values["daly3_mqtt_name"] = os.getenv('DALY3_MQTT_NAME')
            # print ("using env: DALY3_MQTT_NAME")

        values["timescaledb_ip"] = config['DatabaseSection']['timescaledb_ip']
        values["timescaledb_username"] = config['DatabaseSection']['timescaledb_username']
        values["timescaledb_password"] = config['DatabaseSection']['timescaledb_password']
        if os.getenv('TIMESCALEDB_IP', 'None') != 'None':
            values["timescaledb_ip"] = os.getenv('TIMESCALEDB_IP')
            # print ("using env: TIMESCALEDB_IP")
        if os.getenv('TIMESCALEDB_USERNAME', 'None') != 'None':
            values["timescaledb_username"] = os.getenv('TIMESCALEDB_USERNAME')
            # print ("using env: TIMESCALEDB_USERNAME")
        if os.getenv('TIMESCALEDB_PASSWORD', 'None') != 'None':
            values["timescaledb_password"] = os.getenv('TIMESCALEDB_PASSWORD')
            # print ("using env: TIMESCALEDB_PASSWORD")

        values["idm_ip"] = config['IdmSection']['idm_ip']
        values["idm_port"] = int(config['IdmSection']['idm_port'])
        if os.getenv('IDM_IP', 'None') != 'None':
            values["idm_ip"] = os.getenv('IDM_IP')
            # print ("using env: IDM_IP")
        if os.getenv('IDM_PORT', 'None') != 'None':
            values["idm_port"] = int(os.getenv('IDM_PORT'))
            # print ("using env: IDM_PORT")

        values["inverter_ip"] = config['KostalSection']['inverter_ip']
        values["inverter_port"] = int(config['KostalSection']['inverter_port'])
        if os.getenv('INVERTER_IP', 'None') != 'None':
            values["inverter_ip"] = os.getenv('INVERTER_IP')
            # print ("using env: INVERTER_IP")
        if os.getenv('INVERTER_PORT', 'None') != 'None':
            values["inverter_port"] = int(os.getenv('INVERTER_PORT'))
            # print ("using env: INVERTER_PORT")

        values["mqtt_broker"] = config['MqttSection']['mqtt_broker']
        values["mqtt_port"] = int(config['MqttSection']['mqtt_port'])
        values["mqtt_user"] = config['MqttSection']['mqtt_user']
        values["mqtt_password"] = config['MqttSection']['mqtt_password']
        if os.getenv('MQTT_BROKER', 'None') != 'None':
            values["mqtt_broker"] = os.getenv('MQTT_BROKER')
            # print ("using env: MQTT_BROKER")
        if os.getenv('MQTT_PORT', 'None') != 'None':
            values["mqtt_port"] = int(os.getenv('MQTT_PORT'))
            # print ("using env: MQTT_PORT")
        if os.getenv('MQTT_USER', 'None') != 'None':
            values["mqtt_user"] = os.getenv('MQTT_USER')
            # print ("using env: MQTT_USER")
        if os.getenv('MQTT_PASSWORD', 'None') != 'None':
            values["mqtt_password"] = os.getenv('MQTT_PASSWORD')
            # print ("using env: MQTT_PASSWORD")

        # values["solax_tokenid"] = config['SolaxSection']['solax_tokenid']
        # values["solax_inverter"] = config['SolaxSection']['solax_inverter']
        # if os.getenv('SOLAX_TOKENID', 'None') != 'None':
        #     values["solax_tokenid"] = os.getenv('SOLAX_TOKENID')
        #     # print ("using env: SOLAX_TOKENID")
        # if os.getenv('SOLAX_INVERTER', 'None') != 'None':
        #     values["solax_inverter"] = os.getenv('SOLAX_INVERTER')
        #     # print ("using env: SOLAX_INVERTER")

        # values["sems_user"] = config['GoodweSection']['sems_user']
        # values["sems_password"] = config['GoodweSection']['sems_password']
        # values["sems_stationid"] = config['GoodweSection']['sems_stationid']
        # if os.getenv('SEMS_USER', 'None') != 'None':
        #     values["sems_user"] = os.getenv('SEMS_USER')
        #     # print ("using env: SEMS_USER "+values["sems_user"])
        # if os.getenv('SEMS_PASSWORD', 'None') != 'None':
        #     values["sems_password"] = os.getenv('SEMS_PASSWORD')
        #     # print ("using env: SEMS_PASSWORD "+values["sems_password"])
        # if os.getenv('SEMS_STATIONID', 'None') != 'None':
        #     values["sems_stationid"] = os.getenv('SEMS_STATIONID')
        #     # print ("using env: SEMS_STATIONID "+values["sems_stationid"])
        values["goodwe_ip"] = config['GoodweSection']['goodwe_ip']
        if os.getenv('GOODWE_IP', 'None') != 'None':
            values["goodwe_ip"] = os.getenv('GOODWE_IP')
            # print ("using env: GOODWE_IP "+values["goodwe_ip"])

        # print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " config: ", values)

        return values
    except Exception as ex:
        print("ERROR Config: ", ex)
