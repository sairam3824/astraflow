#!/bin/bash

# Test GitHub Documentation Generator Service

echo "Testing GitHub Documentation Generator..."
echo ""

# Test 1: Health check
echo "1. Testing health endpoint..."
curl -s http://localhost:8087/health | python -m json.tool
echo ""

# Test 2: Generate documentation for a sample repository
echo "2. Testing documentation generation..."
curl -X POST http://localhost:8087/generate-docs \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/octocat/Hello-World",
    "license_type": "MIT",
    "generate_readme": true,
    "project_name": "Hello World",
    "project_description": "A simple Hello World repository",
    "author_name": "GitHub User"
  }' | python -m json.tool

echo ""
echo "Test completed!"
