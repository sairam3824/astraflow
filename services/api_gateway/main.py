from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from prometheus_client import make_asgi_app
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from .database import db
from .auth import hash_password, verify_password, create_access_token, get_current_user
from libs.utils.logging import setup_logger
from libs.utils.metrics import http_requests_total, http_request_duration_seconds
import time

logger = setup_logger("api-gateway")

app = FastAPI(title="AstraFlow API Gateway")

# Get templates directory
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup():
    await db.connect()
    logger.info("API Gateway started")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    logger.info("API Gateway stopped")

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response

# Auth Models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Auth Endpoints
@app.post("/auth/register", response_model=TokenResponse)
async def register(req: RegisterRequest):
    user_id = str(uuid.uuid4())
    hashed_pw = hash_password(req.password)
    
    try:
        await db.conn.execute(
            "INSERT INTO users (id, email, hashed_password) VALUES (?, ?, ?)",
            (user_id, req.email, hashed_pw)
        )
        await db.conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    token = create_access_token(user_id)
    logger.info(f"User registered: {req.email}")
    return TokenResponse(access_token=token)

@app.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    cursor = await db.conn.execute(
        "SELECT id, hashed_password FROM users WHERE email = ?",
        (req.email,)
    )
    row = await cursor.fetchone()
    
    if not row or not verify_password(req.password, row[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(row[0])
    logger.info(f"User logged in: {req.email}")
    return TokenResponse(access_token=token)

@app.get("/health")
async def health():
    return {"status": "healthy"}

# HTML Template Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    html_file = TEMPLATES_DIR / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>AstraFlow</h1>")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    html_file = TEMPLATES_DIR / "login.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Login</h1>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    html_file = TEMPLATES_DIR / "dashboard.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Dashboard</h1>")

@app.get("/collections", response_class=HTMLResponse)
async def collections_page():
    html_file = TEMPLATES_DIR / "collections.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Collections</h1>")

@app.get("/workspace", response_class=HTMLResponse)
async def workspace_page():
    html_file = TEMPLATES_DIR / "workspace.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Workspace</h1>")

@app.get("/workflows", response_class=HTMLResponse)
async def workflows_page():
    html_file = TEMPLATES_DIR / "workflows.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Workflows</h1>")

@app.get("/stocks", response_class=HTMLResponse)
async def stocks_page():
    html_file = TEMPLATES_DIR / "stocks.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Stocks</h1>")

@app.get("/settings", response_class=HTMLResponse)
async def settings_page():
    html_file = TEMPLATES_DIR / "settings.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Settings</h1>")

@app.get("/rag", response_class=HTMLResponse)
async def rag_page():
    html_file = TEMPLATES_DIR / "rag.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>RAG Search</h1>")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    html_file = TEMPLATES_DIR / "chat.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Chat</h1>")

# Collection Models
class CreateCollectionRequest(BaseModel):
    name: str
    domain: Optional[str] = None

class CollectionResponse(BaseModel):
    id: str
    name: str
    owner_id: str
    domain: Optional[str] = None
    created_at: str

# Collection API Endpoints
@app.post("/api/collections", response_model=CollectionResponse)
async def create_collection(req: CreateCollectionRequest, user_id: str = Depends(get_current_user)):
    import chromadb
    from libs.utils.config import config
    
    collection_id = str(uuid.uuid4())
    
    try:
        await db.conn.execute(
            "INSERT INTO collections (id, name, owner_id, domain) VALUES (?, ?, ?, ?)",
            (collection_id, req.name, user_id, req.domain)
        )
        await db.conn.commit()
        
        # Initialize ChromaDB collection
        chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)
        chroma_client.create_collection(name=f"collection_{collection_id}")
        
        logger.info(f"Collection created: {collection_id}")
        
        cursor = await db.conn.execute(
            "SELECT * FROM collections WHERE id = ?", (collection_id,)
        )
        row = await cursor.fetchone()
        
        return CollectionResponse(
            id=row[0],
            name=row[1],
            owner_id=row[2],
            domain=row[3],
            created_at=row[4]
        )
    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/collections")
async def list_collections(user_id: str = Depends(get_current_user)):
    cursor = await db.conn.execute(
        "SELECT * FROM collections WHERE owner_id = ?", (user_id,)
    )
    rows = await cursor.fetchall()
    
    return [
        CollectionResponse(
            id=row[0],
            name=row[1],
            owner_id=row[2],
            domain=row[3],
            created_at=row[4]
        )
        for row in rows
    ]

@app.delete("/api/collections/{collection_id}")
async def delete_collection(collection_id: str, user_id: str = Depends(get_current_user)):
    import chromadb
    from libs.utils.config import config
    
    # Verify ownership
    cursor = await db.conn.execute(
        "SELECT owner_id FROM collections WHERE id = ?", (collection_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete from SQLite (cascade will handle related records)
    await db.conn.execute("DELETE FROM collections WHERE id = ?", (collection_id,))
    await db.conn.commit()
    
    # Delete ChromaDB collection
    try:
        chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)
        chroma_client.delete_collection(name=f"collection_{collection_id}")
    except:
        pass
    
    logger.info(f"Collection deleted: {collection_id}")
    return {"status": "deleted"}

# Document Models
class UploadRequest(BaseModel):
    filename: str

class UploadResponse(BaseModel):
    upload_url: str
    object_name: str

class DocumentResponse(BaseModel):
    id: str
    collection_id: str
    filename: str
    status: str
    created_at: str

# Document Endpoints
@app.post("/api/collections/{collection_id}/upload", response_model=UploadResponse)
async def upload_document(collection_id: str, req: UploadRequest, user_id: str = Depends(get_current_user)):
    from .minio_client import minio_client
    
    # Verify collection ownership
    cursor = await db.conn.execute(
        "SELECT owner_id FROM collections WHERE id = ?", (collection_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    doc_id = str(uuid.uuid4())
    object_name = f"{collection_id}/{doc_id}/{req.filename}"
    
    # Generate presigned URL
    upload_url = minio_client.generate_presigned_url(object_name)
    
    # Create document record
    await db.conn.execute(
        "INSERT INTO documents (id, collection_id, filename, status) VALUES (?, ?, ?, ?)",
        (doc_id, collection_id, req.filename, "pending")
    )
    await db.conn.commit()
    
    logger.info(f"Document upload initiated: {doc_id}")
    return UploadResponse(upload_url=upload_url, object_name=object_name)

class IngestRequest(BaseModel):
    object_name: str

@app.post("/api/collections/{collection_id}/ingest")
async def ingest_document(collection_id: str, req: IngestRequest, user_id: str = Depends(get_current_user)):
    from services.celery_worker.celery_app import ingest_document_task
    
    # Verify ownership
    cursor = await db.conn.execute(
        "SELECT owner_id FROM collections WHERE id = ?", (collection_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Extract document_id from object_name (format: collection_id/doc_id/filename)
    parts = req.object_name.split('/')
    if len(parts) >= 2:
        document_id = parts[1]
    else:
        raise HTTPException(status_code=400, detail="Invalid object_name format")
    
    # Trigger ingestion task
    task = ingest_document_task.apply_async(args=[document_id, collection_id, req.object_name])
    
    logger.info(f"Ingestion triggered for document {document_id}")
    return {"job_id": task.id, "status": "processing"}

# Chat Models
class CreateChatSessionRequest(BaseModel):
    model: Optional[str] = None
    collection_id: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    model: Optional[str]
    collection_id: Optional[str]
    created_at: str

class SendMessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: str

# Chat API Endpoints
@app.post("/api/chat/sessions", response_model=ChatSessionResponse)
async def create_chat_session(req: CreateChatSessionRequest, user_id: str = Depends(get_current_user)):
    session_id = str(uuid.uuid4())
    
    await db.conn.execute(
        "INSERT INTO chat_sessions (id, user_id, model, collection_id) VALUES (?, ?, ?, ?)",
        (session_id, user_id, req.model, req.collection_id)
    )
    await db.conn.commit()
    
    cursor = await db.conn.execute(
        "SELECT * FROM chat_sessions WHERE id = ?", (session_id,)
    )
    row = await cursor.fetchone()
    
    logger.info(f"Chat session created: {session_id}")
    return ChatSessionResponse(
        id=row[0],
        user_id=row[1],
        model=row[2],
        collection_id=row[3],
        created_at=row[4]
    )

@app.post("/api/chat/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(session_id: str, req: SendMessageRequest, user_id: str = Depends(get_current_user)):
    # Verify session ownership
    cursor = await db.conn.execute(
        "SELECT user_id, model, collection_id FROM chat_sessions WHERE id = ?", (session_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Store user message
    msg_id = str(uuid.uuid4())
    await db.conn.execute(
        "INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)",
        (msg_id, session_id, "user", req.content)
    )
    await db.conn.commit()
    
    logger.info(f"Message sent in session {session_id}")
    
    cursor = await db.conn.execute(
        "SELECT * FROM chat_messages WHERE id = ?", (msg_id,)
    )
    msg_row = await cursor.fetchone()
    
    return MessageResponse(
        id=msg_row[0],
        session_id=msg_row[1],
        role=msg_row[2],
        content=msg_row[3],
        created_at=msg_row[5]
    )

# RAG Search Endpoint
@app.get("/api/collections/{collection_id}/search")
async def search_collection(
    collection_id: str,
    query: str,
    top_k: int = 5,
    user_id: str = Depends(get_current_user)
):
    import chromadb
    from libs.utils.config import config
    from libs.model_router import get_model
    
    # Verify collection ownership
    cursor = await db.conn.execute(
        "SELECT owner_id FROM collections WHERE id = ?", (collection_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        # Query ChromaDB
        chroma_client = chromadb.HttpClient(host=config.CHROMA_HOST, port=config.CHROMA_PORT)
        collection = chroma_client.get_collection(name=f"collection_{collection_id}")
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'text': doc,
                    'score': 1 - results['distances'][0][i] if results['distances'] else 0,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                })
        
        # Generate AI answer using RAG
        context = "\n\n".join([r['text'] for r in formatted_results])
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        # Get AI model and generate answer
        model = get_model("gpt-4")
        answer = model.generate(prompt)
        
        logger.info(f"RAG search performed on collection {collection_id}")
        
        return {
            "answer": answer,
            "results": formatted_results,
            "query": query
        }
        
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    from libs.utils.config import config
    uvicorn.run(app, host="0.0.0.0", port=config.API_GATEWAY_PORT)
