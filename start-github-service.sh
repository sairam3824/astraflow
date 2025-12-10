#!/bin/bash

echo "Starting GitHub Analysis Service..."
echo ""

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the service
cd services/github_analysis
python main.py
