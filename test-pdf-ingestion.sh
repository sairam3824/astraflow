#!/bin/bash

# Test script for PDF ingestion pipeline
# Usage: ./test-pdf-ingestion.sh <pdf_file_path>

set -e

API_URL="http://localhost:8080"
PDF_FILE="${1:-sample.pdf}"

echo "=== PDF Ingestion Test ==="
echo "PDF File: $PDF_FILE"
echo ""

# Step 1: Register/Login
echo "Step 1: Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@astraflow.com",
    "password": "admin123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "Login failed. Trying to register..."
  REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "admin@astraflow.com",
      "password": "admin123"
    }')
  TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.access_token')
fi

echo "Token: ${TOKEN:0:20}..."
echo ""

# Step 2: Create Collection
echo "Step 2: Creating collection..."
COLLECTION_RESPONSE=$(curl -s -X POST "$API_URL/api/collections" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Documents",
    "domain": "General"
  }')

COLLECTION_ID=$(echo $COLLECTION_RESPONSE | jq -r '.id')
echo "Collection ID: $COLLECTION_ID"
echo ""

# Step 3: Get Upload URL
echo "Step 3: Getting upload URL..."
UPLOAD_RESPONSE=$(curl -s -X POST "$API_URL/api/collections/$COLLECTION_ID/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"filename\": \"$(basename $PDF_FILE)\"
  }")

UPLOAD_URL=$(echo $UPLOAD_RESPONSE | jq -r '.upload_url')
OBJECT_NAME=$(echo $UPLOAD_RESPONSE | jq -r '.object_name')
echo "Upload URL obtained"
echo "Object Name: $OBJECT_NAME"
echo ""

# Step 4: Upload PDF
echo "Step 4: Uploading PDF..."
if [ -f "$PDF_FILE" ]; then
  curl -s -X PUT -T "$PDF_FILE" "$UPLOAD_URL"
  echo "PDF uploaded successfully"
else
  echo "Error: PDF file not found: $PDF_FILE"
  exit 1
fi
echo ""

# Step 5: Trigger Ingestion
echo "Step 5: Triggering ingestion..."
INGEST_RESPONSE=$(curl -s -X POST "$API_URL/api/collections/$COLLECTION_ID/ingest" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"object_name\": \"$OBJECT_NAME\"
  }")

JOB_ID=$(echo $INGEST_RESPONSE | jq -r '.job_id')
DOCUMENT_ID=$(echo $INGEST_RESPONSE | jq -r '.document_id')
echo "Job ID: $JOB_ID"
echo "Document ID: $DOCUMENT_ID"
echo ""

# Step 6: Monitor Status
echo "Step 6: Monitoring ingestion status..."
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS_RESPONSE=$(curl -s -X GET "$API_URL/api/documents/$DOCUMENT_ID/status" \
    -H "Authorization: Bearer $TOKEN")
  
  STATUS=$(echo $STATUS_RESPONSE | jq -r '.status')
  CHUNKS=$(echo $STATUS_RESPONSE | jq -r '.chunks')
  
  echo "Attempt $((ATTEMPT+1))/$MAX_ATTEMPTS - Status: $STATUS, Chunks: $CHUNKS"
  
  if [ "$STATUS" == "indexed" ]; then
    echo ""
    echo "✓ Document successfully indexed!"
    echo "Total chunks: $CHUNKS"
    break
  elif [ "$STATUS" == "failed" ]; then
    echo ""
    echo "✗ Document ingestion failed!"
    exit 1
  fi
  
  ATTEMPT=$((ATTEMPT+1))
  sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
  echo ""
  echo "⚠ Timeout waiting for ingestion to complete"
  exit 1
fi
echo ""

# Step 7: Test RAG Query
echo "Step 7: Testing RAG query..."
QUERY="What is this document about?"
SEARCH_RESPONSE=$(curl -s -X GET "$API_URL/api/collections/$COLLECTION_ID/search?query=$(echo $QUERY | jq -sRr @uri)&top_k=3" \
  -H "Authorization: Bearer $TOKEN")

echo "Query: $QUERY"
echo ""
echo "Answer:"
echo $SEARCH_RESPONSE | jq -r '.answer'
echo ""
echo "Top 3 relevant chunks:"
echo $SEARCH_RESPONSE | jq -r '.results[] | "- Score: \(.score | tonumber | . * 100 | round / 100) | \(.text[:100])..."'
echo ""

echo "=== Test Complete ==="
echo ""
echo "Collection ID: $COLLECTION_ID"
echo "Document ID: $DOCUMENT_ID"
echo ""
echo "You can now query this collection with:"
echo "curl -X GET '$API_URL/api/collections/$COLLECTION_ID/search?query=YOUR_QUESTION' \\"
echo "  -H 'Authorization: Bearer $TOKEN'"
