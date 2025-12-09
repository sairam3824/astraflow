#!/bin/bash

# Test script for Chat Service with LangChain Memory

echo "Testing Chat Service..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Base URLs
CHAT_SERVICE="http://localhost:8090"
API_GATEWAY="http://localhost:8080"

# Test 1: Create a chat session
echo -e "${YELLOW}1. Creating chat session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "model": "gpt-4",
    "system_prompt": "You are a helpful assistant."
  }')

echo "$SESSION_RESPONSE" | jq .
echo ""

# Test 2: Send first message
echo -e "${YELLOW}2. Sending first message...${NC}"
MSG1_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "message": "Hello! What is 2+2?",
    "model": "gpt-4"
  }')

echo "$MSG1_RESPONSE" | jq .
echo ""

# Test 3: Send follow-up message (tests memory)
echo -e "${YELLOW}3. Sending follow-up message (testing memory)...${NC}"
MSG2_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "message": "What was my previous question?",
    "model": "gpt-4"
  }')

echo "$MSG2_RESPONSE" | jq .
echo ""

# Test 4: Get conversation history
echo -e "${YELLOW}4. Getting conversation history...${NC}"
HISTORY_RESPONSE=$(curl -s "$CHAT_SERVICE/sessions/test-session-123/history")

echo "$HISTORY_RESPONSE" | jq .
echo ""

# Test 5: List all sessions
echo -e "${YELLOW}5. Listing all sessions...${NC}"
SESSIONS_RESPONSE=$(curl -s "$CHAT_SERVICE/sessions")

echo "$SESSIONS_RESPONSE" | jq .
echo ""

# Test 6: Delete session
echo -e "${YELLOW}6. Deleting session...${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "$CHAT_SERVICE/sessions/test-session-123")

echo "$DELETE_RESPONSE" | jq .
echo ""

echo -e "${GREEN}✓ Chat service tests completed!${NC}"
echo ""
echo "Note: Make sure the chat service is running on port 8090"
echo "Run: python -m services.chat_service.main"
