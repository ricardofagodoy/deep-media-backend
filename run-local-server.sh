#!/bin/bash

source env.sh

cd src
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 wsgi:app