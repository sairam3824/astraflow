from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Collection(BaseModel):
    id: str
    name: str
    owner_id: str
    domain: Optional[str] = None
    created_at: datetime

class Document(BaseModel):
    id: str
    collection_id: str
    filename: str
    pages: Optional[int] = None
    status: str = "pending"
    summary_id: Optional[str] = None
    created_at: datetime

class Chunk(BaseModel):
    id: str
    doc_id: str
    text: str
    tokens: int
    offset: int
    created_at: datetime

class Vector(BaseModel):
    chunk_id: str
    doc_id: str
    collection_id: str
    embedding: List[float]

class Workflow(BaseModel):
    id: str
    name: str
    collection_id: Optional[str] = None
    definition: Dict
    created_at: datetime

class WorkflowNode(BaseModel):
    id: str
    type: str
    params: Dict

class GitHubRepository(BaseModel):
    id: str
    repo_url: str
    user_id: str
    readme_content: Optional[str] = None
    license_recommendation: Optional[str] = None
    analysis_data: Optional[Dict] = None
    status: str = "pending"
    created_at: datetime

class ChatSession(BaseModel):
    id: str
    user_id: str
    model: Optional[str] = None
    collection_id: Optional[str] = None
    created_at: datetime

class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    tokens: Optional[int] = None
    created_at: datetime

class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    created_at: datetime

class Summary(BaseModel):
    id: str
    doc_id: str
    content: str
    model: str
    created_at: datetime

class StockTick(BaseModel):
    symbol: str
    price: float
    volume: int
    timestamp: datetime

class Indicators(BaseModel):
    symbol: str
    sma_20: Optional[float] = None
    ema_12: Optional[float] = None
    vwap: Optional[float] = None
    volatility: Optional[float] = None
    timestamp: datetime
