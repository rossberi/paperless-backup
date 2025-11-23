#!/bin/sh

if [ -n "$BACKUP_SCHEDULE" ]; then
    printf "\n"
    printf "BACKUP_SCHEDULE detected: $BACKUP_SCHEDULE\n"
    printf "Next backup scheduled at: $(date -d "$BACKUP_SCHEDULE")\n"
    printf "\n"

    # create crontab
    echo "$BACKUP_SCHEDULE /usr/local/bin/python3 /code/main.py >> /var/log/backup.log 2>&1" > /etc/crontabs/root
    exec crond -f

else
    printf "No BACKUP_SCHEDULE detected. Starting backup ..."
    exec /usr/local/bin/python3 /code/main.py
fi
