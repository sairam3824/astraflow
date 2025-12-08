#!/bin/bash
# Initialize MinIO buckets

mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/documents --ignore-existing
mc mb local/github-repos --ignore-existing

echo "MinIO buckets initialized"
