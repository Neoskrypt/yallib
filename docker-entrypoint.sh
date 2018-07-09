#!/bin/bash
set -e
CELERYPID=/var/run/celery/worker1.pid [[ -f "$CELERYPID" ]] && rm -f "$CELERYPID"
/etc/init.d/celery start
exec "$@"
