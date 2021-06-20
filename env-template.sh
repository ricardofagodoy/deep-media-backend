#!/bin/bash

echo "Setting environment variables..."
export PORT=5000
export FLASK_DEBUG=1

# Needs access to Firebase Authentication, Datastore Database and Cloud Scheduler
export GOOGLE_APPLICATION_CREDENTIALS="$(PWD)/service-account-file.json"

# Scheduler Configs
export PROJECT_ID="deepmedia-2021-06-11"
export LOCATION_ID="southamerica-east1"
export TIMEZONE="America/Sao_Paulo"
export OPTIMIZERS_TOPIC="optimizations"
export OPTIMIZERS_CRON="0 */1 * * *"

# Google Connector
export GOOGLE_CLIENT_ID=""
export GOOGLE_CLIENT_SECRET=""
export GOOGLE_DEVELOPER_TOKEN=""