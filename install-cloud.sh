#!/bin/bash

# Builds docker image
IMAGE_URL=gcr.io/deep-media/deep-media-backend:latest
gcloud builds submit --tag $IMAGE_URL

# Update Datastore indexes
gcloud datastore indexes create index.yaml --quiet

# Enable needed APIs
gcloud services enable googleads.googleapis.com
gcloud services enable datastore.googleapis.com
gcloud services enable analytics.googleapis.com

# Grant service account access to act as another one
# gcloud iam service-accounts add-iam-policy-binding [SERVICE_ACCOUNT] --member [MEMBER_EMAIL] --role roles/iam.serviceAccountUser

# Deploy to Cloud Run
gcloud run deploy --image $IMAGE_URL --platform managed