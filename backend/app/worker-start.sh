#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

#celery worker -A app.worker -l info -Q main-queue -c 5 -O fair --pidfile /tmp/celeryd.pid -D
#celery beat -s /tmp/celerybeat-schedule --pidfile /tmp/celerybeat.pid
