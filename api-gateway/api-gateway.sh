#!/bin/bash

API_ID=backend
API_CONFIG_ID=backend_api
GCP_REGION=us-central1
CURRENT_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com

gcloud api-gateway api-configs create $API_CONFIG_ID \
  --api=$API_ID --openapi-spec=openapi2-run.yaml \
  --project="$CURRENT_PROJECT"

gcloud api-gateway gateways create GATEWAY_ID \
  --api=$API_ID --api-config=$API_CONFIG_ID \
  --location=$GCP_REGION --project="$CURRENT_PROJECT"