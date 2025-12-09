# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Services

```bash
./start-all.sh
```

Wait about 30 seconds for all services to start.

### Step 2: Login or Register

1. Open your browser: http://localhost:8080
2. Click "Login" or go directly to: http://localhost:8080/login
3. **Register** a new account:
   - Enter your email (e.g., `user@example.com`)
   - Enter a password
   - Click "Register"
4. You'll be automatically logged in and redirected to the dashboard

### Step 3: Start Chatting!

1. Click "Chat" in the sidebar
2. Click "+ New Chat" button
3. Select an AI model:
   - **Gemini Pro** (Google) - Free tier available ✅
   - **GPT-4** (OpenAI) - Most capable
   - **GPT-3.5 Turbo** - Fast and affordable
4. Click "Start Chat"
5. Type your message and press Enter!

## 🎉 You're Done!

Try asking:
- "What is 2+2?"
- "My name is Alice"
- "What's my name?" (tests memory)

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ Python 3.11+ installed
- ✅ Docker and Docker Compose installed
- ✅ API keys in `.env` file:
  ```bash
  OPENAI_API_KEY=sk-your-key-here
  GEMINI_API_KEY=your-gemini-key-here
  ```

## 🔧 Troubleshooting

### "Please login first"

**Solution:** Go to http://localhost:8080/login and register/login

### "Error creating chat session"

**Check:**
1. Are you logged in?
2. Is the chat service running?
   ```bash
   curl http://localhost:8090/health
   ```
3. Check logs:
   ```bash
   tail -f logs/chat_service.log
   ```

### Services not starting

```bash
# Stop everything
./stop-all.sh

# Start fresh
./start-all.sh

# Check status
curl http://localhost:8080/health
curl http://localhost:8090/health
```

### Port already in use

```bash
# Find what's using the port
lsof -i :8080
lsof -i :8090

# Kill the process
kill -9 <PID>
```

## 📚 Next Steps

Once you're chatting:

1. **Test Memory:**
   ```
   You: My favorite color is blue
   AI: That's nice!
   You: What's my favorite color?
   AI: Your favorite color is blue
   ```

2. **Try Different Models:**
   - Use the dropdown to switch between GPT-4 and Gemini
   - Compare their responses!

3. **Upload Documents:**
   - Go to "Collections"
   - Create a collection
   - Upload PDFs
   - Chat about your documents (coming soon)

## 🎯 Common Tasks

### Create a New Chat Session

1. Click "+ New Chat"
2. Select model
3. Click "Start Chat"

### Switch Models

Use the dropdown at the bottom of the chat to switch between models mid-conversation.

### View Logs

```bash
# All logs
tail -f logs/*.log

# Just chat service
tail -f logs/chat_service.log

# Just API gateway
tail -f logs/api_gateway.log
```

### Stop Services

```bash
./stop-all.sh
```

## 📖 Documentation

- **CHAT_USER_GUIDE.md** - Detailed user guide
- **CHAT_IMPLEMENTATION.md** - Technical details
- **TROUBLESHOOTING.md** - Common issues
- **GEMINI_INTEGRATION.md** - Gemini setup

## ✅ Success Checklist

- [ ] Services started with `./start-all.sh`
- [ ] Registered/logged in at http://localhost:8080/login
- [ ] Opened chat page at http://localhost:8080/chat
- [ ] Created a new chat session
- [ ] Sent a message
- [ ] Received AI response
- [ ] Tested conversation memory

## 🎊 You're All Set!

Enjoy chatting with AI! The system remembers your entire conversation, so you can have natural, flowing discussions.

**Need help?** Check the troubleshooting guide or documentation files.
