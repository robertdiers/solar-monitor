#FROM docker.io/debian:stable
#FROM docker.io/python
FROM docker.io/ubuntu:24.04

RUN apt update
RUN apt -y upgrade
#RUN apt -y install gcc cron python3 python3-pip libpq-dev python3-dev
RUN apt -y install gcc cron libpq-dev python3-dev python3-pip
RUN pip install pymodbus==3.7.4 pyserial_asyncio pyserial psycopg2-binary paho-mqtt requests --break-system-packages
#RUN python3 -m venv ~/.local --system-site-packages
#RUN ~/.local/bin/pip install configparser
#RUN ~/.local/bin/pip install pymodbus
#RUN ~/.local/bin/pip install psycopg2-binary
#RUN ~/.local/bin/pip install paho-mqtt
#RUN ~/.local/bin/pip install pyserial
#RUN ~/.local/bin/pip install pyserial_asyncio
#RUN ~/.local/bin/pip install requests

RUN which python3

# copy files
COPY python /app/python
COPY shell/daly-subscribe.sh /app/daly-subscribe.sh
COPY shell/solar-monitor.sh /app/solar-monitor.sh
COPY shell/entrypoint.sh /app/entrypoint.sh
COPY shell/container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]
