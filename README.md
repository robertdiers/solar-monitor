# solar-monitor

## Setup:
* Kostal Plenticore 10 inverter
* BYD HVS storage
* Kostal energy meter
* iDM Heat Pump AERO SLM 6-17 with "solar input" feature
* Solax Mini inverter
* GoodWe 5048D-ES inverter with Tasmota Sonoff POW R3
* 48V battery block with Daly BMS (3 blocks in parallel)
* Tasmota device with temperature sensor (Sonoff TH16 + DS18B20)
* Device to run the containers

## main Python scripts (startup and cron triggered):
* init.py - initializes TimescaleDB tables as they are removed when device restarts
* daly-subscribe.py - subscribes to DALY MQTT output and store to database (https://github.com/softwarecrash/DALY-BMS-to-MQTT)
* solar-monitor.py - collect metrics and store to database

## additional Python modules
* BYD.py - read actual values from BYD battery (TCP Socket)
* Config.py - read config file and check for environment parameter overrides
* Daly.py - subscribes to MQTT topic to read data
* Goodwe.py - read actual values from Goodwe inverter (SEMS Portal API)
* IdmPump.py - read actual solar power from iDM heat pump (TCP Modbus)
* Kostal.py - read actual values from Kostal inverter (TCP Modbus)
* Solax.py - read actual values from Solax inverter (Solax Portal API)
* Tasmota.py - read Tasmota data (MQTT)
* TimescaleDb.py - write to TimescaleDB

Hint: data input for iDM is realized with dedicated container: https://github.com/robertdiers/kostal_idmpump

## Docker

please override config values using environment variables

```
docker run -d --restart always --name solarmonitor -e MQTT_PASSWORD=password ghcr.io/robertdiers/solar-monitor:1.12
```

### TimescaleDB (please define your own password)
Using tmpfs to store data in memory, sd card doesn't have to store it:

```
docker run -d --restart always --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password --mount type=tmpfs,destination=/var/lib/postgresql/data timescale/timescaledb:latest-pg14
```

### Grafana
Dashboard JSON is placed in this repo:

```
docker run -d --name grafana --volume "$PWD/grafanadata:/var/lib/grafana" -p 3000:3000 --restart always grafana/grafana:latest
```

### EMQX (MQTT broker, please define your own password)
```
docker run -d --name emqx -p 18083:18083 -p 1883:1883 -v $PWD/emqxdata:/opt/emqx/data --restart always emqx:latest
```

