#!/bin/sh

flask create-tables && \
    gunicorn --bind $HOST:$PORT \
             --workers $WORKERS \
             shorturl:app
