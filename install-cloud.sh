#!/bin/bash

CURRENT_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

# Builds docker image
IMAGE_URL=gcr.io/$CURRENT_PROJECT/deep-media-backend:latest
gcloud builds submit --tag "$IMAGE_URL"

# Update Datastore indexes
gcloud datastore indexes create index.yaml --quiet

# Enable needed APIs
gcloud services enable googleads.googleapis.com
gcloud services enable datastore.googleapis.com
gcloud services enable analytics.googleapis.com
gcloud services enable pubsub.googleapis.com

# Deploy to Cloud Run
gcloud beta run services replace service.yaml --region southamerica-east1