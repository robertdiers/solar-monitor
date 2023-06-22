#FROM docker.io/debian:stable-slim
FROM docker.io/python

#RUN apt update
#RUN apt -y upgrade
#RUN apt -y install gcc cron python3 python3-pip libpq-dev python3-dev
RUN apt-get update && apt-get -y install cron
RUN pip3 install configparser
RUN pip3 install pymodbus 
RUN pip3 install psycopg2
RUN pip3 install paho-mqtt
RUN pip3 install pyserial_asyncio
RUN pip3 install pyserial
RUN pip3 install requests

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
