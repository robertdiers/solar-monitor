#!/usr/bin/env python

# import asyncio
import goodwe
import TimescaleDb


class Goodwe:

    async def get_runtime_data(goodwe_ip):

        inverter = await goodwe.connect(goodwe_ip)
        runtime_data = await inverter.read_runtime_data()

        for sensor in inverter.sensors():
            if sensor.id_ in runtime_data:
                # print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
                if 'temperature' in sensor.id_ and 'battery_' not in sensor.id_:
                    TimescaleDb.writeT('goodwe_temp', runtime_data[sensor.id_])
                if 'vbattery1' in sensor.id_:
                    TimescaleDb.writeV('goodwe_battery_volt', runtime_data[sensor.id_])
                if 'pbattery1' in sensor.id_:
                    TimescaleDb.writeW('goodwe_battery_watt', runtime_data[sensor.id_])
                if 'battery_soh' in sensor.id_:
                    TimescaleDb.writeP('goodwe_battery_soh', runtime_data[sensor.id_])
                if 'battery_soc' in sensor.id_:
                    TimescaleDb.writeP('goodwe_battery_soc', runtime_data[sensor.id_])
                if 'pgrid' in sensor.id_:
                    TimescaleDb.writeW('goodwe_grid', runtime_data[sensor.id_])
                if 'e_day' in sensor.id_:
                    TimescaleDb.writeK('goodwe_dailyyield', runtime_data[sensor.id_])
                    TimescaleDb.writeKT('goodwe_dailyyield', runtime_data[sensor.id_])
                if 'e_load_day' in sensor.id_:
                    TimescaleDb.writeK('goodwe_load_dailyyield', runtime_data[sensor.id_])
                # need to be careful with in statement
                if 'ppv1' in sensor.id_:
                    TimescaleDb.writeW('goodwe_pv_1', runtime_data[sensor.id_])
                elif 'ppv2' in sensor.id_:
                    TimescaleDb.writeW('goodwe_pv_2', runtime_data[sensor.id_])
                elif 'ppv' in sensor.id_:
                    TimescaleDb.writeW('goodwe_pv', runtime_data[sensor.id_])
