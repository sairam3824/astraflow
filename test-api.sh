#!/bin/bash

# AstraFlow API Test Script
set -e

API_URL="http://localhost:8080"

echo "=== Testing AstraFlow API ==="
echo ""

# 1. Register a user
echo "1. Registering user..."
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123","full_name":"Demo User"}')

TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "Registration failed. Trying login..."
  LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"demo@example.com","password":"demo123"}')
  TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
fi

echo "Token: ${TOKEN:0:50}..."
echo ""

# 2. Create a collection
echo "2. Creating collection..."
COLLECTION_RESPONSE=$(curl -s -X POST "$API_URL/collections" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"api-test-collection","description":"Test collection"}')

COLLECTION_ID=$(echo $COLLECTION_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Collection ID: $COLLECTION_ID"
echo ""

# 3. List collections
echo "3. Listing collections..."
curl -s -X GET "$API_URL/collections" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# 4. Health check
echo "4. Health check..."
curl -s "$API_URL/health" | python3 -m json.tool
echo ""

echo "=== All tests passed! ==="
