#!/bin/sh

# Check if BACKUP_SCHEDULE is set
if [ -n "$BACKUP_SCHEDULE" ]; then
    printf "\n"
    printf "BACKUP_SCHEDULE detected: $BACKUP_SCHEDULE\n"
    printf "\n"

    # create crontab
    echo "$BACKUP_SCHEDULE /usr/local/bin/python3 /code/main.py >> /proc/1/fd/1 2>&1" > /etc/crontabs/root
    crond -f -L /dev/stdout

else
    printf "No BACKUP_SCHEDULE detected. Starting backup ..."
    exec /usr/local/bin/python3 /code/main.py
fi
