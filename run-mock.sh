#!/bin/bash

# Define local environment variables
source env.sh

export MOCK=1

echo "Starting app..."
python src/main.py
