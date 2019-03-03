#!/bin/bash
NAME="weighttracker"                                    # Name of the application
PORT=8080                                         # port to bind to
DJANGODIR=/home/pi/weighttracker
USER=pi                                         # the user to run as
GROUP=pi                                        # the group to run as
TIMEOUT=120                                       # when I should give up
DJANGO_SETTINGS_MODULE=weighttracker.settings           # which settings file should Django use
DJANGO_WSGI_MODULE=weighttracker.wsgi

echo "Starting $NAME as `whoami`"

# Setenv the Python env
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR

ARGS="${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers 4 \
  --user=$USER 
  --group=$GROUP \
  --log-level info \
  --bind=0.0.0.0:$PORT \
  --timeout $TIMEOUT \
  --limit-request-line 0 \
  --reload
"

# Start your Django Unicorn
exec gunicorn ${ARGS}

