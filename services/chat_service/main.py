from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("chat-service")

app = FastAPI(title="Chat Service")

# In-memory storage for chat sessions and their message histories
chat_sessions: Dict[str, ChatMessageHistory] = {}
session_metadata: Dict[str, dict] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: Optional[str] = "gpt-4"


class ChatResponse(BaseModel):
    session_id: str
    message: str
    role: str = "assistant"
    timestamp: str


class CreateSessionRequest(BaseModel):
    model: Optional[str] = "gpt-4"
    system_prompt: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    model: str
    created_at: str


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "chat-service"}


class CreateSessionWithIdRequest(BaseModel):
    session_id: str
    model: Optional[str] = "gpt-4"
    system_prompt: Optional[str] = None


@app.post("/sessions", response_model=SessionResponse)
async def create_session(req: CreateSessionWithIdRequest):
    """Create a new chat session with memory using provided session_id"""
    session_id = req.session_id
    
    # Initialize message history for this session
    chat_sessions[session_id] = ChatMessageHistory()
    
    # Store session metadata
    session_metadata[session_id] = {
        "model": req.model or "gpt-4",
        "created_at": datetime.utcnow().isoformat(),
        "system_prompt": req.system_prompt
    }
    
    # Add system message if provided
    if req.system_prompt:
        chat_sessions[session_id].add_message(SystemMessage(content=req.system_prompt))
    
    logger.info(f"Created chat session: {session_id} with model {req.model}")
    
    return SessionResponse(
        session_id=session_id,
        model=req.model or "gpt-4",
        created_at=session_metadata[session_id]["created_at"]
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a message and get AI response with conversation memory"""
    
    if req.session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Get session info
        metadata = session_metadata[req.session_id]
        history = chat_sessions[req.session_id]
        
        # Add user message to history
        history.add_user_message(req.message)
        
        # Initialize LLM based on model
        model_name = metadata["model"]
        
        if model_name in ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]:
            # Use Gemini
            llm = ChatGoogleGenerativeAI(
                model=model_name if model_name != "gemini-pro" else "gemini-1.5-pro",
                temperature=0.7,
                google_api_key=config.GEMINI_API_KEY
            )
        else:
            # Use OpenAI (default)
            llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                openai_api_key=config.OPENAI_API_KEY
            )
        
        # Get all messages from history
        messages = history.messages
        
        # Get AI response
        response = llm.invoke(messages)
        
        # Add AI response to history
        history.add_ai_message(response.content)
        
        logger.info(f"Chat response generated for session {req.session_id}")
        
        return ChatResponse(
            session_id=req.session_id,
            message=response.content,
            role="assistant",
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}/history")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = chat_sessions[session_id]
    messages = []
    
    for msg in history.messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        elif isinstance(msg, SystemMessage):
            role = "system"
        else:
            role = "unknown"
        
        messages.append({
            "role": role,
            "content": msg.content
        })
    
    return {
        "session_id": session_id,
        "messages": messages,
        "total": len(messages)
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session and its history"""
    
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del chat_sessions[session_id]
    del session_metadata[session_id]
    
    logger.info(f"Deleted chat session: {session_id}")
    
    return {"status": "deleted", "session_id": session_id}


@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    
    sessions = []
    for session_id, metadata in session_metadata.items():
        message_count = len(chat_sessions[session_id].messages)
        sessions.append({
            "session_id": session_id,
            "model": metadata["model"],
            "created_at": metadata["created_at"],
            "message_count": message_count
        })
    
    return {"sessions": sessions, "total": len(sessions)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
