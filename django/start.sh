#!/bin/bash

# Waiting for MySQL database to be ready ...
db_cmd="mysql -h ${DB_HOST} -u ${MYSQL_USER} "-p${MYSQL_PASSWORD}""
counter=1

while ! ${db_cmd} -e "show databases;" > /dev/null 2>&1; do
    sleep 1
    counter=$(expr ${counter} + 1)
done
echo "[Django]" $(date "+%Y/%m/%d-%H:%M:%S") MySQL database ready! "(${counter}sec)"

# update permission
if [ -e /media ]; then
    chmod 777 /media
fi

# start supervisor
echo "[supervisord]" $(date "+%Y/%m/%d-%H:%M:%S") start
exec /usr/bin/supervisord -c /data/supervisord/supervisord.conf
