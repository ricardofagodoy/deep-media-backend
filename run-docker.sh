#!/bin/bash

IMAGE=deep-media-backend
source env.sh

docker build -t $IMAGE .

docker run --rm \
  -e GOOGLE_APPLICATION_CREDENTIALS="/var/service-account-file.json" \
  --mount type=bind,source=$(PWD)/service-account-file.json,target=/var/service-account-file.json \
  -e PROJECT_ID \
  -e LOCATION_ID \
  -e TIMEZONE \
  -e OPTIMIZERS_TOPIC \
  -e OPTIMIZERS_CRON \
  -e GOOGLE_CLIENT_ID \
  -e GOOGLE_CLIENT_SECRET \
  -e GOOGLE_DEVELOPER_TOKEN \
  -e PORT \
  -p "$PORT":"$PORT" \
  $IMAGE:latest