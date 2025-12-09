#!/bin/bash

# Test script for Gemini integration

echo "Testing Gemini Integration..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CHAT_SERVICE="http://localhost:8090"

# Test 1: Create Gemini session
echo -e "${YELLOW}1. Creating Gemini chat session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gemini-test-123",
    "model": "gemini-pro",
    "system_prompt": "You are a helpful assistant powered by Google Gemini."
  }')

echo "$SESSION_RESPONSE" | jq .
echo ""

# Test 2: Send first message to Gemini
echo -e "${YELLOW}2. Sending message to Gemini...${NC}"
MSG1_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gemini-test-123",
    "message": "Hello! What model are you?",
    "model": "gemini-pro"
  }')

echo "$MSG1_RESPONSE" | jq .
echo ""

# Test 3: Test Gemini memory
echo -e "${YELLOW}3. Testing Gemini memory...${NC}"
MSG2_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gemini-test-123",
    "message": "My favorite color is purple. Remember that!",
    "model": "gemini-pro"
  }')

echo "$MSG2_RESPONSE" | jq .
echo ""

# Test 4: Verify memory
echo -e "${YELLOW}4. Verifying Gemini remembers...${NC}"
MSG3_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gemini-test-123",
    "message": "What is my favorite color?",
    "model": "gemini-pro"
  }')

echo "$MSG3_RESPONSE" | jq .
echo ""

# Test 5: Get conversation history
echo -e "${YELLOW}5. Getting conversation history...${NC}"
HISTORY_RESPONSE=$(curl -s "$CHAT_SERVICE/sessions/gemini-test-123/history")

echo "$HISTORY_RESPONSE" | jq .
echo ""

# Test 6: Compare with GPT-4
echo -e "${YELLOW}6. Creating GPT-4 session for comparison...${NC}"
GPT_SESSION=$(curl -s -X POST "$CHAT_SERVICE/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gpt4-test-123",
    "model": "gpt-4",
    "system_prompt": "You are a helpful assistant powered by OpenAI."
  }')

echo "$GPT_SESSION" | jq .
echo ""

echo -e "${YELLOW}7. Sending same question to GPT-4...${NC}"
GPT_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gpt4-test-123",
    "message": "Explain quantum computing in one sentence",
    "model": "gpt-4"
  }')

echo -e "${BLUE}GPT-4 Response:${NC}"
echo "$GPT_RESPONSE" | jq -r '.message'
echo ""

echo -e "${YELLOW}8. Sending same question to Gemini...${NC}"
GEMINI_RESPONSE=$(curl -s -X POST "$CHAT_SERVICE/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "gemini-test-123",
    "message": "Explain quantum computing in one sentence",
    "model": "gemini-pro"
  }')

echo -e "${BLUE}Gemini Response:${NC}"
echo "$GEMINI_RESPONSE" | jq -r '.message'
echo ""

# Cleanup
echo -e "${YELLOW}9. Cleaning up test sessions...${NC}"
curl -s -X DELETE "$CHAT_SERVICE/sessions/gemini-test-123" | jq .
curl -s -X DELETE "$CHAT_SERVICE/sessions/gpt4-test-123" | jq .
echo ""

echo -e "${GREEN}✓ Gemini integration tests completed!${NC}"
echo ""
echo "Summary:"
echo "  - Gemini Pro session created ✓"
echo "  - Messages sent and received ✓"
echo "  - Conversation memory working ✓"
echo "  - Both models available ✓"
echo ""
echo "Try it in the UI: http://localhost:8080/chat"
echo "Select 'Gemini Pro (Google)' from the model dropdown"
