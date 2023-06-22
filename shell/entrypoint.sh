printenv | grep -v "no_proxy" >> /etc/environment
/usr/local/bin/python3 -V
echo 'environment stored - waiting for timescaledb'
sleep 60
cd /app/python
echo 'starting database init'
/usr/local/bin/python3 init.py
echo 'starting cron'
cd /app
cron -f