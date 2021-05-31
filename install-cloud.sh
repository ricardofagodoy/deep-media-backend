#!/bin/bash

IMAGE_URL=gcr.io/deep-media/deep-media-backend:latest

gcloud builds submit --tag $IMAGE_URL

gcloud run deploy --image $IMAGE_URL --platform managed