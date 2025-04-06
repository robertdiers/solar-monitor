# solar-monitor

## Setup:
* Kostal Plenticore 10 inverter
* BYD HVS storage
* Kostal energy meter
* iDM Heat Pump AERO SLM 6-17 with "solar input" feature
* multiple Solax Mini inverters (power metered by Shelly PM Mini G3)
* GoodWe 5048D-ES inverter with Tasmota Sonoff POW R3
* 48V battery block with Daly BMS (3 blocks in parallel)
* Tasmota device with temperature sensor (Sonoff TH16 + DS18B20)
* Device to run the containers

## main Python scripts (startup and cron triggered):
* init.py - initializes TimescaleDB tables as they are removed when device restarts
* daly-subscribe.py - subscribes to DALY MQTT output and store to database (https://github.com/softwarecrash/DALY-BMS-to-MQTT)
* shelly-subscribe.py - subscribes to Shelly MQTT output (SolaX inverters)
* solar-monitor.py - collect metrics and store to database

## additional Python modules
* BYD.py - read actual values from BYD battery (TCP Socket)
* Config.py - read config file and check for environment parameter overrides
* Daly.py - subscribes to MQTT topic to read data
* Goodwe.py - read actual values from Goodwe inverter (SEMS Portal API) - UNUSED
* Goodwe_Local.py - read actual values from Goodwe inverter (python package)
* IdmPump.py - read actual solar power from iDM heat pump (TCP Modbus)
* Kostal.py - read actual values from Kostal inverter (TCP Modbus)
* Shelly.py - subscribes to MQTT topic to read data
* Solax.py - read actual values from Solax inverter (Solax Portal API) - UNUSED
* Tasmota.py - read Tasmota data (MQTT)
* TimescaleDb.py - write to TimescaleDB

Hint: data input for iDM is realized with dedicated container: https://github.com/robertdiers/kostal_idmpump

## Docker Compose

please override config values using environment variables (see python/solar-monitor.ini)

```
services:
    solarmonitor:
        image: ghcr.io/robertdiers/solar-monitor:1.25
        container_name: solarmonitor
        restart: always
        environment:
        - MQTT_BROKER=brokerip
        - MQTT_PASSWORD=brokerpassword
        - TIMESCALEDB_IP=databaseip
        - TIMESCALEDB_PASSWORD=databasepassword
        - BYD_IP=bydip
        - IDM_IP=idmip
        - INVERTER_IP=kostalip
        - GOODWE_IP=goodweip
```

### TimescaleDB (please define your own password)

Using tmpfs to store data in memory, disc doesn't have to store it:

```
services:
  timescaledb:
    image: docker.io/timescale/timescaledb:latest-pg14
    container_name: timescaledb
    restart: always
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD=yourpassword 
    tmpfs:
      - /var/lib/postgresql/data
```

### Grafana

Dashboard JSON is placed in this repo:

```
services:
    grafana:
        image: docker.io/grafana/grafana:latest
        container_name: grafana
        restart: always
        ports:
        - 3000:3000
        volumes:
        - ${PWD}/grafanadata:/var/lib/grafana
```

### Mosquitto (MQTT broker, please define your config and password file once)

https://be-jo.net/2024/01/mqtt-broker-mosquitto-als-docker-container-installieren/

mosquitto.conf

```
persistence false
log_dest stdout
password_file /mosquitto/config/mosquitto.passwd
allow_anonymous false
listener 1883
```

container:

```
services:
  mosquitto:
      image: docker.io/eclipse-mosquitto:latest
      container_name: mosquitto
      restart: always
      volumes:
        - folderwithyourconfigandpasswordfile:/mosquitto/config
      ports:
        - 1883:1883
        - 9001:9001
```

after running the container you can create your own user and password using this command - than restart the container:

```
mosquitto_passwd -c /mosquitto/config/mosquitto.passwd youruser
```
