from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from prometheus_client import make_asgi_app
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
import asyncio
import httpx

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
    first_name: Optional[str] = None
    last_name: Optional[str] = None

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
            "INSERT INTO users (id, email, hashed_password, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
            (user_id, req.email, hashed_pw, req.first_name, req.last_name)
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
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>AstraFlow</h1>")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    html_file = TEMPLATES_DIR / "login.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Login</h1>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    html_file = TEMPLATES_DIR / "dashboard.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Dashboard</h1>")

@app.get("/collections", response_class=HTMLResponse)
async def collections_page():
    html_file = TEMPLATES_DIR / "collections.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Collections</h1>")

@app.get("/workspace", response_class=HTMLResponse)
async def workspace_page():
    html_file = TEMPLATES_DIR / "workspace.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Workspace</h1>")

@app.get("/workflows", response_class=HTMLResponse)
async def workflows_page():
    html_file = TEMPLATES_DIR / "workflows.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Workflows</h1>")

@app.get("/stocks", response_class=HTMLResponse)
async def stocks_page():
    html_file = TEMPLATES_DIR / "stocks.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Stocks</h1>")

@app.get("/settings", response_class=HTMLResponse)
async def settings_page():
    html_file = TEMPLATES_DIR / "settings.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Settings</h1>")

@app.get("/rag", response_class=HTMLResponse)
async def rag_page():
    html_file = TEMPLATES_DIR / "rag.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>RAG Search</h1>")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    html_file = TEMPLATES_DIR / "chat.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>Chat</h1>")

@app.get("/github-docs", response_class=HTMLResponse)
async def github_docs_page():
    html_file = TEMPLATES_DIR / "github_docs.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding='utf-8'))
    return HTMLResponse(content="<h1>GitHub Documentation Generator</h1>")

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
    
    # Update document status to processing
    await db.conn.execute(
        "UPDATE documents SET status = 'processing' WHERE id = ?",
        (document_id,)
    )
    await db.conn.commit()
    
    # Trigger ingestion task
    task = ingest_document_task.apply_async(args=[document_id, collection_id, req.object_name])
    
    logger.info(f"Ingestion triggered for document {document_id}")
    return {"job_id": task.id, "status": "processing", "document_id": document_id}

@app.get("/api/collections/{collection_id}/documents")
async def list_documents(collection_id: str, user_id: str = Depends(get_current_user)):
    """List all documents in a collection"""
    # Verify ownership
    cursor = await db.conn.execute(
        "SELECT owner_id FROM collections WHERE id = ?", (collection_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get documents
    cursor = await db.conn.execute(
        "SELECT id, filename, status, created_at FROM documents WHERE collection_id = ? ORDER BY created_at DESC",
        (collection_id,)
    )
    rows = await cursor.fetchall()
    
    documents = [
        {
            "id": row[0],
            "filename": row[1],
            "status": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]
    
    return {"documents": documents, "total": len(documents)}

@app.get("/api/documents/{document_id}/status")
async def get_document_status(document_id: str, user_id: str = Depends(get_current_user)):
    """Get document processing status"""
    cursor = await db.conn.execute(
        """
        SELECT d.id, d.filename, d.status, d.created_at, c.owner_id
        FROM documents d
        JOIN collections c ON d.collection_id = c.id
        WHERE d.id = ?
        """,
        (document_id,)
    )
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if row[4] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get chunk count
    cursor = await db.conn.execute(
        "SELECT COUNT(*) FROM chunks WHERE doc_id = ?",
        (document_id,)
    )
    chunk_count = (await cursor.fetchone())[0]
    
    return {
        "id": row[0],
        "filename": row[1],
        "status": row[2],
        "created_at": row[3],
        "chunks": chunk_count
    }

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
    model = req.model or "gpt-4"
    
    # Create session in database
    await db.conn.execute(
        "INSERT INTO chat_sessions (id, user_id, model, collection_id) VALUES (?, ?, ?, ?)",
        (session_id, user_id, model, req.collection_id)
    )
    await db.conn.commit()
    
    # Initialize session in chat service with LangChain memory
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://localhost:8090/sessions",
                json={
                    "session_id": session_id,
                    "model": model,
                    "system_prompt": "You are a helpful AI assistant. Provide clear, accurate, and friendly responses."
                },
                timeout=10.0
            )
    except Exception as e:
        logger.error(f"Error initializing chat service session: {e}")
        # Continue anyway, session will be created on first message
    
    cursor = await db.conn.execute(
        "SELECT * FROM chat_sessions WHERE id = ?", (session_id,)
    )
    row = await cursor.fetchone()
    
    logger.info(f"Chat session created: {session_id} with model {model}")
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
    
    session_model = row[1] or "gpt-4"
    
    # Store user message
    msg_id = str(uuid.uuid4())
    await db.conn.execute(
        "INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)",
        (msg_id, session_id, "user", req.content)
    )
    await db.conn.commit()
    
    logger.info(f"Message sent in session {session_id}")
    
    # Call chat service to get AI response
    try:
        async with httpx.AsyncClient() as client:
            chat_response = await client.post(
                "http://localhost:8090/chat",
                json={
                    "session_id": session_id,
                    "message": req.content,
                    "model": session_model
                },
                timeout=30.0
            )
            
            if chat_response.status_code == 200:
                ai_response = chat_response.json()
                
                # Store AI response
                ai_msg_id = str(uuid.uuid4())
                await db.conn.execute(
                    "INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)",
                    (ai_msg_id, session_id, "assistant", ai_response["message"])
                )
                await db.conn.commit()
                
                logger.info(f"AI response stored for session {session_id}")
                
                # Return the AI response
                cursor = await db.conn.execute(
                    "SELECT * FROM chat_messages WHERE id = ?", (ai_msg_id,)
                )
                ai_msg_row = await cursor.fetchone()
                
                return MessageResponse(
                    id=ai_msg_row[0],
                    session_id=ai_msg_row[1],
                    role=ai_msg_row[2],
                    content=ai_msg_row[3],
                    created_at=ai_msg_row[5]
                )
            else:
                raise HTTPException(status_code=500, detail="Chat service error")
                
    except Exception as e:
        logger.error(f"Error calling chat service: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get AI response: {str(e)}")

class UpdateModelRequest(BaseModel):
    model: str

@app.patch("/api/chat/sessions/{session_id}/model")
async def update_chat_model(session_id: str, req: UpdateModelRequest, user_id: str = Depends(get_current_user)):
    # Verify session ownership
    cursor = await db.conn.execute(
        "SELECT user_id FROM chat_sessions WHERE id = ?", (session_id,)
    )
    row = await cursor.fetchone()
    
    if not row or row[0] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update model
    await db.conn.execute(
        "UPDATE chat_sessions SET model = ? WHERE id = ?",
        (req.model, session_id)
    )
    await db.conn.commit()
    
    logger.info(f"Chat session {session_id} model updated to {req.model}")
    return {"status": "updated", "model": req.model}

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
        
        try:
            collection = chroma_client.get_collection(name=f"collection_{collection_id}")
            
            # Check if collection has any documents
            count = collection.count()
            if count == 0:
                return {
                    "answer": "This collection is empty. Please upload and index some documents first.",
                    "results": [],
                    "query": query
                }
            
            results = collection.query(
                query_texts=[query],
                n_results=min(top_k, count)
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
            
            if not formatted_results:
                return {
                    "answer": "No relevant documents found for your query.",
                    "results": [],
                    "query": query
                }
            
            # Generate AI answer using RAG
            context = "\n\n".join([r['text'] for r in formatted_results])
            prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
            
            # Use OpenAI directly for now
            from openai import OpenAI
            openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            logger.info(f"RAG search performed on collection {collection_id}")
            
            return {
                "answer": answer,
                "results": formatted_results,
                "query": query,
                "total_chunks": count
            }
            
        except Exception as e:
            if "does not exist" in str(e).lower():
                return {
                    "answer": "This collection has not been initialized yet. Please upload and index some documents first.",
                    "results": [],
                    "query": query
                }
            raise
        
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Stock API Endpoints
@app.get("/api/stocks/quote/{symbol}")
async def get_stock_quote(symbol: str):
    """Get real-time stock quote from stock producer service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8085/quote/{symbol}")
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch quote")
    except Exception as e:
        logger.error(f"Error fetching stock quote: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/start-stream")
async def start_stock_stream():
    """Start streaming stock data from Alpha Vantage"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8085/start-stream")
            return response.json()
    except Exception as e:
        logger.error(f"Error starting stock stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks/stop-stream")
async def stop_stock_stream():
    """Stop streaming stock data"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8085/stop-stream")
            return response.json()
    except Exception as e:
        logger.error(f"Error stopping stock stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stocks/stream-status")
async def get_stream_status():
    """Get streaming status"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8085/stream-status")
            return response.json()
    except Exception as e:
        logger.error(f"Error getting stream status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket for real-time stock updates
class StockWebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.kafka_consumer = None
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to websocket: {e}")

stock_ws_manager = StockWebSocketManager()

@app.websocket("/ws/stocks")
async def websocket_stocks(websocket: WebSocket):
    """WebSocket endpoint for real-time stock data"""
    await stock_ws_manager.connect(websocket)
    consumer = None
    
    try:
        # Start consuming from Kafka in background
        from kafka import KafkaConsumer
        from libs.utils.config import config
        import asyncio
        
        consumer = KafkaConsumer(
            'market.ticks',
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='websocket-stock-consumer',
            consumer_timeout_ms=1000  # Timeout to prevent blocking
        )
        
        # Send messages to websocket with non-blocking polling
        while True:
            # Poll for messages with timeout
            messages = consumer.poll(timeout_ms=100, max_records=10)
            
            if messages:
                for topic_partition, records in messages.items():
                    for message in records:
                        try:
                            await websocket.send_json(message.value)
                        except WebSocketDisconnect:
                            raise
                        except Exception as e:
                            logger.error(f"Error sending stock data: {e}")
            
            # Yield control to event loop
            await asyncio.sleep(0.01)
                
    except WebSocketDisconnect:
        stock_ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        stock_ws_manager.disconnect(websocket)
    finally:
        if consumer:
            consumer.close()

if __name__ == "__main__":
    import uvicorn
    from libs.utils.config import config
    uvicorn.run(app, host="0.0.0.0", port=config.API_GATEWAY_PORT)
