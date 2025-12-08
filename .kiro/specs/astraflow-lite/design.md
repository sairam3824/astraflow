# AstraFlow Lite - Design Document

## Overview

AstraFlow Lite is a locally-hosted AI platform that provides document management, RAG capabilities, multi-model chat, workflow automation, stock analysis, and GitHub repository documentation generation. The system is built as a microservices architecture running on Docker Compose with SQLite for metadata, ChromaDB/FAISS for vectors, Kafka for stock streaming, and Celery for background tasks.

### Key Design Principles

1. **Local-First**: All services run locally without cloud dependencies (except external LLM API calls)
2. **Modular Architecture**: Independent microservices with clear boundaries and responsibilities
3. **Extensibility**: Model router and adapters designed to easily add new LLM providers
4. **Asynchronous Processing**: Long-running tasks handled by Celery to maintain responsiveness
5. **Per-Collection Isolation**: Vector indices and RAG queries scoped to individual Collections

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                    (Next.js + TailwindCSS)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                       │
│                    JWT Auth + Route Aggregation                  │
└─┬───────┬──────────┬──────────┬──────────┬──────────┬──────────┘
  │       │          │          │          │          │
  ▼       ▼          ▼          ▼          ▼          ▼
┌───┐  ┌────┐    ┌─────┐   ┌──────┐   ┌──────┐   ┌────────┐
│Ing│  │Emb │    │Agent│   │Work  │   │Stock │   │GitHub  │
│est│  │edd │    │Rout │   │flow  │   │Svc   │   │Analysis│
│ion│  │ing │    │er   │   │Runner│   │      │   │        │
└─┬─┘  └─┬──┘    └──┬──┘   └──┬───┘   └──┬───┘   └───┬────┘
  │      │          │         │          │           │
  ▼      ▼          ▼         ▼          ▼           ▼
┌──────────────────────────────────────────────────────────┐
│                    Storage Layer                          │
│  ┌────────┐  ┌──────────┐  ┌──────┐  ┌──────┐  ┌─────┐ │
│  │ SQLite │  │ChromaDB/ │  │MinIO │  │Redis │  │Kafka│ │
│  │        │  │  FAISS   │  │      │  │      │  │     │ │
│  └────────┘  └──────────┘  └──────┘  └──────┘  └─────┘ │
└──────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Celery Workers  │
                    │  (Background)   │
                    └─────────────────┘
```

### Service Communication Patterns

1. **Synchronous**: API Gateway → Microservices (HTTP REST)
2. **Asynchronous**: Celery task queue for long-running operations
3. **Event Streaming**: Kafka for stock tick data only
4. **Real-time**: WebSocket/SSE for chat streaming and stock updates

## Components and Interfaces

### 1. API Gateway

**Responsibilities:**
- Single entry point for all client requests
- JWT token validation and user authentication
- Request routing to appropriate microservices
- WebSocket/SSE connection management for streaming

**Key Endpoints:**
```
POST   /auth/login
POST   /auth/register
GET    /collections
POST   /collections
DELETE /collections/{id}
POST   /collections/{id}/upload
POST   /collections/{id}/ingest
GET    /collections/{id}/search
POST   /chat/sessions
POST   /chat/sessions/{id}/messages
GET    /chat/sessions/{id}/stream (SSE)
POST   /workflows
POST   /workflows/{id}/run
GET    /stocks/{symbol}/indicators
POST   /github/analyze
GET    /github/analysis/{id}
```

**Dependencies:**
- SQLite (user accounts, sessions)
- Redis (session cache)
- All microservices

### 2. Ingestion Service

**Responsibilities:**
- Accept document uploads via presigned URLs
- Extract text from PDFs using pdfminer/tika
- Apply OCR (Tesseract) for scanned documents
- Perform semantic chunking with overlap
- Store raw documents in MinIO
- Create Document and Chunk records in SQLite

**Key Operations:**
```python
async def ingest_document(doc_id: str, collection_id: str) -> IngestResult:
    # 1. Download from MinIO
    # 2. Extract text (PDF/OCR)
    # 3. Semantic chunking
    # 4. Store chunks in SQLite
    # 5. Trigger embedding service
    pass
```

**Dependencies:**
- MinIO (document storage)
- SQLite (metadata)
- Celery (async execution)

### 3. Embedding Service

**Responsibilities:**
- Generate embeddings for text chunks
- Call OpenAI embedding API or local sentence-transformers
- Upsert vectors into ChromaDB/FAISS per Collection
- Maintain Collection-specific vector indices

**Key Operations:**
```python
async def embed_chunks(chunk_ids: List[str], collection_id: str) -> EmbedResult:
    # 1. Fetch chunks from SQLite
    # 2. Call embedding provider
    # 3. Upsert to ChromaDB/FAISS collection
    # 4. Update chunk status
    pass
```

**Dependencies:**
- SQLite (chunk data)
- ChromaDB or FAISS (vector storage)
- OpenAI API (embeddings)

### 4. Agent Router Service

**Responsibilities:**
- Orchestrate RAG queries and chat responses
- Retrieve relevant chunks from vector store
- Build prompts with context
- Route to appropriate LLM (GPT or Gemini)
- Manage chat session state

**Key Operations:**
```python
async def handle_chat_message(
    session_id: str,
    message: str,
    collection_id: Optional[str]
) -> ChatResponse:
    # 1. Retrieve from vector store if collection specified
    # 2. Build prompt with context
    # 3. Route to model (GPT/Gemini)
    # 4. Stream response
    # 5. Store in chat history
    pass
```

**Dependencies:**
- ChromaDB/FAISS (retrieval)
- SQLite (chat history)
- Model Adapter (LLM calls)

### 5. Model Adapter Layer

**Responsibilities:**
- Unified interface for LLM providers
- Implement adapters for GPT and Gemini
- Handle API authentication and rate limiting
- Log token usage and costs
- Support streaming responses

**Interface:**
```python
class ModelAdapter(ABC):
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        model: str,
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        pass
    
    @abstractmethod
    def estimate_cost(self, tokens: int) -> float:
        pass
```

**Implementations:**
- `OpenAIAdapter` (GPT-3.5, GPT-4)
- `GeminiAdapter` (Gemini Pro, Gemini Ultra)

### 6. Model Router

**Responsibilities:**
- Select appropriate model based on task or user preference
- Implement routing policies (cost, speed, accuracy)
- Task classification for automatic routing

**Routing Logic:**
```python
def select_model(
    task_type: Optional[str],
    user_preference: Optional[str],
    context_length: int
) -> str:
    if user_preference:
        return user_preference
    
    # Automatic routing
    if task_type == "summarization":
        return "gemini-pro"  # Cost-effective
    elif context_length > 8000:
        return "gpt-4-turbo"  # Large context
    else:
        return "gpt-3.5-turbo"  # Fast and cheap
```

### 7. Workflow Runner Service

**Responsibilities:**
- Execute LangGraph workflow definitions
- Validate workflow structure
- Orchestrate node execution (retrieve, llm, postprocess)
- Handle workflow state and error recovery

**Supported Node Types:**
- `retrieve`: Query vector store
- `llm`: Call model adapter
- `postprocess`: Extract entities, format output
- `notify`: Send notifications (future)

**Workflow Execution:**
```python
async def run_workflow(workflow_id: str, inputs: Dict) -> WorkflowResult:
    # 1. Load workflow definition
    # 2. Validate structure
    # 3. Execute nodes via LangGraph
    # 4. Return results
    pass
```

### 8. Stock Services

#### Stock Producer
**Responsibilities:**
- Ingest real-time or simulated stock data
- Publish ticks to Kafka topic `market.ticks`
- Partition by symbol for parallel processing

#### Stock Analysis Service
**Responsibilities:**
- Consume from `market.ticks`
- Compute indicators (SMA, EMA, VWAP, volatility)
- Publish to `market.indicators`
- Store latest values in Redis

**Indicator Computation:**
```python
def compute_indicators(ticks: List[Tick]) -> Indicators:
    df = pd.DataFrame(ticks)
    return Indicators(
        sma_20=df['price'].rolling(20).mean().iloc[-1],
        ema_12=df['price'].ewm(span=12).mean().iloc[-1],
        vwap=calculate_vwap(df),
        volatility=df['price'].std()
    )
```

### 9. GitHub Analysis Service

**Responsibilities:**
- Clone or fetch GitHub repository contents
- Analyze codebase structure and file types
- Extract dependencies from package files
- Generate README using LLM
- Recommend licenses based on project characteristics

**Analysis Pipeline:**
```python
async def analyze_repository(repo_url: str) -> GitHubAnalysis:
    # 1. Clone repository (shallow)
    # 2. Analyze structure (languages, frameworks)
    # 3. Extract dependencies
    # 4. Generate README via LLM
    # 5. Recommend license
    # 6. Store results
    pass
```

**README Generation Prompt:**
```
Analyze this repository structure and generate a comprehensive README:

Repository: {repo_name}
Languages: {languages}
Files: {file_tree}
Dependencies: {dependencies}

Generate a README with:
1. Project description
2. Installation instructions
3. Usage examples
4. API documentation (if applicable)
5. Contributing guidelines
```

### 10. Celery Task Manager

**Responsibilities:**
- Execute background tasks asynchronously
- Retry failed tasks with exponential backoff
- Schedule periodic tasks (via Celery Beat or n8n)

**Task Types:**
- `ingest_document_task`
- `embed_chunks_task`
- `summarize_document_task`
- `run_workflow_task`
- `analyze_github_repo_task`

**Configuration:**
```python
CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'task_track_started': True,
    'task_time_limit': 3600,
    'task_soft_time_limit': 3000,
}
```

## Data Models

### SQLite Schema

```sql
-- Users
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Collections
CREATE TABLE collections (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    domain TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id),
    UNIQUE(owner_id, name)
);

-- Documents
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    collection_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    pages INTEGER,
    status TEXT DEFAULT 'pending',
    summary_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
);

-- Chunks
CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    text TEXT NOT NULL,
    tokens INTEGER,
    offset INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    model TEXT,
    collection_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (collection_id) REFERENCES collections(id)
);

-- Chat Messages
CREATE TABLE chat_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
);

-- Workflows
CREATE TABLE workflows (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    collection_id TEXT,
    definition JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (collection_id) REFERENCES collections(id)
);

-- Summaries
CREATE TABLE summaries (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    content TEXT NOT NULL,
    model TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- GitHub Analyses
CREATE TABLE github_analyses (
    id TEXT PRIMARY KEY,
    repo_url TEXT NOT NULL,
    user_id TEXT NOT NULL,
    readme_content TEXT,
    license_recommendation TEXT,
    analysis_data JSON,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Pydantic Models

```python
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

class ChatSession(BaseModel):
    id: str
    user_id: str
    model: Optional[str] = None
    collection_id: Optional[str] = None
    created_at: datetime

class ChatMessage(BaseModel):
    id: str
    session_id: str
    role: str  # "user" or "assistant"
    content: str
    tokens: Optional[int] = None
    created_at: datetime

class Workflow(BaseModel):
    id: str
    name: str
    collection_id: Optional[str] = None
    definition: Dict  # LangGraph JSON
    created_at: datetime

class WorkflowNode(BaseModel):
    id: str
    type: str  # "retrieve", "llm", "postprocess", "notify"
    params: Dict

class GitHubAnalysis(BaseModel):
    id: str
    repo_url: str
    user_id: str
    readme_content: Optional[str] = None
    license_recommendation: Optional[str] = None
    analysis_data: Optional[Dict] = None
    status: str = "pending"
    created_at: datetime
```

### Vector Store Structure (ChromaDB/FAISS)

Each Collection has its own vector index:

```python
# ChromaDB Collection naming
collection_name = f"collection_{collection_id}"

# Vector metadata
{
    "chunk_id": "k1",
    "doc_id": "d1",
    "collection_id": "c1",
    "text": "original chunk text",
    "tokens": 120
}
```

## 
Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Collection Management Properties

**Property 1: Collection creation produces valid records**
*For any* valid Collection name and optional domain, creating a Collection should result in a record with a unique identifier, timestamp, and correct owner association.
**Validates: Requirements 1.1**

**Property 2: Collection isolation**
*For any* user, requesting Collections should return only Collections owned by that user and no Collections owned by other users.
**Validates: Requirements 1.2, 10.3**

**Property 3: Cascade deletion**
*For any* Collection with associated documents, chunks, and vectors, deleting the Collection should remove all related data from SQLite and the vector index.
**Validates: Requirements 1.3**

**Property 4: Unique Collection names per user**
*For any* user, attempting to create two Collections with the same name should result in the second creation being rejected.
**Validates: Requirements 1.4**

**Property 5: Vector index initialization**
*For any* newly created Collection, querying its vector index should return zero results until documents are embedded.
**Validates: Requirements 1.5**

### Document Ingestion Properties

**Property 6: Presigned URL generation**
*For any* Collection and document upload request, the system should return a valid presigned URL that can be used to upload to MinIO.
**Validates: Requirements 2.1**

**Property 7: Document record creation**
*For any* completed document upload, a Document record should exist in SQLite with filename, pending status, and Collection association.
**Validates: Requirements 2.2**

**Property 8: Text extraction completeness**
*For any* valid document, ingestion should produce non-empty text content that can be chunked.
**Validates: Requirements 2.3**

**Property 9: Semantic chunking produces valid chunks**
*For any* extracted text, chunking should produce Chunk records where each chunk has non-empty text, positive token count, and valid offset.
**Validates: Requirements 2.5**

### Embedding and Indexing Properties

**Property 10: Vector generation**
*For any* chunk, the embedding service should generate a vector with the expected dimensionality for the chosen embedding model.
**Validates: Requirements 3.2**

**Property 11: Vector index membership**
*For any* embedded chunk, querying the Collection's vector index should return that chunk's vector with correct metadata.
**Validates: Requirements 3.3**

**Property 12: Vector metadata completeness**
*For any* vector in a Collection index, the metadata should include chunk_id and collection_id fields.
**Validates: Requirements 3.4**

**Property 13: Document status transition**
*For any* document, once all its chunks have been embedded, the document status should be updated to "ingested".
**Validates: Requirements 3.5**

### RAG and Search Properties

**Property 14: Top-k retrieval**
*For any* search query on a Collection, the system should return at most k chunks, and all returned chunks should belong to that Collection.
**Validates: Requirements 4.1**

**Property 15: Prompt structure**
*For any* RAG query with retrieved chunks, the constructed prompt should contain the user query, retrieved chunk texts, and system instructions.
**Validates: Requirements 4.2**

**Property 16: Model selection consistency**
*For any* request with an explicit model preference, the Model Router should select that exact model.
**Validates: Requirements 4.3, 14.1**

**Property 17: Search result structure**
*For any* search query, the response should include a list of retrieved chunks with metadata and optionally an AI-generated answer.
**Validates: Requirements 4.5**

### Chat Session Properties

**Property 18: Chat session creation**
*For any* chat session creation request, a session record should exist with the specified model preference and optional Collection association.
**Validates: Requirements 5.1**

**Property 19: Message persistence**
*For any* message sent in a chat session, that message should appear in the chat history with correct role, content, and timestamp.
**Validates: Requirements 5.2**

**Property 20: Collection-aware retrieval**
*For any* chat session associated with a Collection, sending a message should trigger retrieval from that Collection's vector index.
**Validates: Requirements 5.3**

**Property 21: Chat response streaming and storage**
*For any* chat response, the response should be both streamed to the client and stored in the chat history.
**Validates: Requirements 5.5**

### Workflow Properties

**Property 22: Workflow definition storage**
*For any* workflow creation, the workflow definition should be stored as valid JSON and be retrievable.
**Validates: Requirements 6.1**

**Property 23: Workflow validation**
*For any* workflow execution request, invalid workflow structures should be rejected before execution begins.
**Validates: Requirements 6.3**

**Property 24: Workflow node execution order**
*For any* valid workflow, nodes should execute in the order defined by the workflow graph edges.
**Validates: Requirements 6.4**

**Property 25: Workflow completion**
*For any* completed workflow execution, results should be returned and the execution status should be updated.
**Validates: Requirements 6.5**

### Summarization Properties

**Property 26: Summary task creation**
*For any* completed PDF ingestion, a Celery task for summarization should be created.
**Validates: Requirements 7.1**

**Property 27: Summary record association**
*For any* generated summary, a Summary record should exist in SQLite associated with the correct Document.
**Validates: Requirements 7.3**

**Property 28: Summary regeneration**
*For any* summary regeneration request, a new Celery task should be created and executed.
**Validates: Requirements 7.4**

### Stock Analysis Properties

**Property 29: Kafka tick publishing**
*For any* market data received by the Stock Producer, tick records should appear in the Kafka topic partitioned by symbol.
**Validates: Requirements 8.1**

**Property 30: Indicator computation**
*For any* set of stock ticks, the Stock Analysis Service should compute SMA, EMA, VWAP, and volatility values.
**Validates: Requirements 8.2**

**Property 31: Indicator storage**
*For any* computed indicators, the values should be stored in both the Kafka indicators topic and Redis.
**Validates: Requirements 8.3**

**Property 32: Indicator retrieval**
*For any* symbol with computed indicators, requesting indicators should return the latest values from Redis.
**Validates: Requirements 8.4**

### Task Management Properties

**Property 33: Task retry with backoff**
*For any* failing Celery task, retries should occur with exponentially increasing delays up to the configured maximum attempts.
**Validates: Requirements 9.5**

### Authentication and Authorization Properties

**Property 34: JWT validation**
*For any* API request, invalid or expired JWT tokens should be rejected with an appropriate error response.
**Validates: Requirements 10.1, 10.5**

**Property 35: Collection ownership**
*For any* created Collection, the owner_id should match the authenticated user's identifier.
**Validates: Requirements 10.2**

**Property 36: Collection access authorization**
*For any* Collection access attempt, users should only be able to access Collections they own.
**Validates: Requirements 10.4**

### Logging and Monitoring Properties

**Property 37: Structured logging**
*For any* operation in any microservice, logs should be emitted in valid JSON format with required fields (timestamp, level, service, message).
**Validates: Requirements 12.1**

**Property 38: LLM call logging**
*For any* LLM API call, a log entry should exist containing the model used, token count, and estimated cost.
**Validates: Requirements 12.4**

**Property 39: Task failure logging**
*For any* failed Celery task, a log entry should exist with the task name, parameters, and stack trace.
**Validates: Requirements 12.5**

### GitHub Analysis Properties

**Property 40: Repository cloning**
*For any* valid GitHub repository URL, the system should successfully clone or fetch the repository contents.
**Validates: Requirements 15.1**

**Property 41: Codebase analysis**
*For any* cloned repository, analysis should produce data about file types, languages, and dependencies.
**Validates: Requirements 15.2**

**Property 42: README generation**
*For any* analyzed repository, a README should be generated containing non-empty content.
**Validates: Requirements 15.3**

**Property 43: README section completeness**
*For any* generated README, it should contain sections for project description, installation, usage, and contribution guidelines.
**Validates: Requirements 15.4**

**Property 44: License recommendation**
*For any* analyzed repository, a license recommendation should be provided based on project characteristics.
**Validates: Requirements 15.5**

**Property 45: Analysis result storage**
*For any* completed GitHub analysis, the README and license recommendation should be stored and retrievable from SQLite.
**Validates: Requirements 15.6**

### Schema Validation Properties

**Property 46: Request validation**
*For any* API request, invalid data that doesn't match the Pydantic schema should be rejected with detailed validation errors.
**Validates: Requirements 16.2**

**Property 47: Validation error detail**
*For any* schema validation failure, the error response should include specific field names and validation messages.
**Validates: Requirements 16.4**

**Property 48: Response serialization**
*For any* API response, the data should be serialized using Pydantic models ensuring type safety.
**Validates: Requirements 16.5**

## Error Handling

### Error Categories

1. **Client Errors (4xx)**
   - Invalid input data (400)
   - Authentication failures (401)
   - Authorization failures (403)
   - Resource not found (404)
   - Duplicate resource (409)

2. **Server Errors (5xx)**
   - Internal service errors (500)
   - External API failures (502)
   - Service unavailable (503)
   - Task timeout (504)

### Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "collection.name",
        "message": "Field required"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

### Retry Strategies

**Celery Tasks:**
```python
@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(APIError, NetworkError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def embed_chunks_task(self, chunk_ids, collection_id):
    try:
        # Task logic
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
```

**External API Calls:**
- Exponential backoff with jitter
- Maximum 3 retries for transient failures
- Circuit breaker for repeated failures
- Fallback to alternative providers when possible

### Graceful Degradation

1. **Vector Search Failures**: Return empty results with error flag
2. **LLM API Failures**: Return cached response or error message
3. **Kafka Unavailable**: Buffer stock data in Redis temporarily
4. **Embedding Service Down**: Queue chunks for later processing

## Testing Strategy

### Unit Testing

**Framework**: pytest with pytest-asyncio for async tests

**Coverage Areas:**
- Pydantic model validation
- Utility functions (chunking, text extraction)
- Model router selection logic
- Indicator calculation functions
- Prompt construction
- Error handling paths

**Example Unit Tests:**
```python
def test_semantic_chunking():
    text = "Long document text..."
    chunks = semantic_chunk(text, max_tokens=512, overlap=50)
    assert all(chunk.tokens <= 512 for chunk in chunks)
    assert len(chunks) > 0

def test_model_router_explicit_selection():
    router = ModelRouter()
    model = router.select_model(user_preference="gpt-4")
    assert model == "gpt-4"

def test_collection_name_uniqueness():
    # Test that duplicate names are rejected
    pass
```

### Property-Based Testing

**Framework**: Hypothesis (Python)

**Configuration**: Minimum 100 iterations per property test

**Test Tagging**: Each property test must include a comment with the format:
```python
# Feature: astraflow-lite, Property 1: Collection creation produces valid records
@given(collection_name=st.text(min_size=1, max_size=100))
def test_collection_creation_property(collection_name):
    # Test implementation
    pass
```

**Key Property Tests:**

1. **Collection Management** (Properties 1-5)
   - Generate random Collection names and domains
   - Verify creation, isolation, deletion, uniqueness, and initialization

2. **Document Ingestion** (Properties 6-9)
   - Generate random documents and text content
   - Verify URL generation, record creation, extraction, and chunking

3. **Embedding and Indexing** (Properties 10-13)
   - Generate random chunks
   - Verify vector generation, indexing, metadata, and status updates

4. **RAG and Search** (Properties 14-17)
   - Generate random queries and Collections
   - Verify retrieval count, prompt structure, model selection, and response format

5. **Chat Sessions** (Properties 18-21)
   - Generate random messages and sessions
   - Verify session creation, message persistence, retrieval, and streaming

6. **Workflows** (Properties 22-25)
   - Generate random workflow definitions
   - Verify storage, validation, execution order, and completion

7. **Summarization** (Properties 26-28)
   - Generate random documents
   - Verify task creation, summary association, and regeneration

8. **Stock Analysis** (Properties 29-32)
   - Generate random stock ticks
   - Verify Kafka publishing, indicator computation, storage, and retrieval

9. **Task Management** (Property 33)
   - Simulate task failures
   - Verify retry behavior with exponential backoff

10. **Authentication** (Properties 34-36)
    - Generate random tokens and user IDs
    - Verify validation, ownership, and authorization

11. **Logging** (Properties 37-39)
    - Generate random operations
    - Verify log format, LLM logging, and failure logging

12. **GitHub Analysis** (Properties 40-45)
    - Generate random repository structures
    - Verify cloning, analysis, README generation, sections, licenses, and storage

13. **Schema Validation** (Properties 46-48)
    - Generate random valid and invalid data
    - Verify validation, error details, and serialization

### Integration Testing

**Test Scenarios:**
1. End-to-end document ingestion: Upload → Extract → Chunk → Embed → Search
2. Chat session with RAG: Create session → Send message → Retrieve → Generate → Stream
3. Workflow execution: Create workflow → Execute → Verify results
4. Stock pipeline: Produce ticks → Consume → Compute → Store → Retrieve
5. GitHub analysis: Submit URL → Clone → Analyze → Generate → Store

**Test Environment:**
- Docker Compose with all services
- Test database (separate SQLite file)
- Test vector store (separate ChromaDB collection)
- Mock LLM providers for deterministic testing

### Performance Testing

**Load Testing:**
- Concurrent document uploads (100 simultaneous)
- High-frequency stock ticks (1000 ticks/second)
- Multiple chat sessions (50 concurrent)

**Benchmarks:**
- Document ingestion: < 5 seconds per 10-page PDF
- Vector search: < 100ms for top-10 retrieval
- Chat response: < 2 seconds for first token
- Indicator computation: < 50ms per symbol

## Deployment Architecture

### Docker Compose (Development)

```yaml
version: '3.8'

services:
  api-gateway:
    build: ./services/api_gateway
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/data
    depends_on:
      - redis
      - minio
      - chromadb

  ingestion:
    build: ./services/ingestion
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
      - MINIO_URL=minio:9000
    volumes:
      - ./data:/data

  embedding:
    build: ./services/embedding
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
      - CHROMADB_URL=http://chromadb:8000
    volumes:
      - ./data:/data

  agent-router:
    build: ./services/agent_router
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
      - CHROMADB_URL=http://chromadb:8000
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./data:/data

  workflow-runner:
    build: ./services/workflow_runner
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
    volumes:
      - ./data:/data

  stocks-producer:
    build: ./services/stocks_producer
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092

  stocks-analysis:
    build: ./services/stocks_analysis
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
      - REDIS_URL=redis://redis:6379

  github-analysis:
    build: ./services/github_analysis
    environment:
      - DATABASE_URL=sqlite:///data/astraflow.db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./data:/data
      - ./repos:/repos

  celery-worker:
    build: ./services/celery_worker
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - DATABASE_URL=sqlite:///data/astraflow.db
    volumes:
      - ./data:/data

  frontend:
    build: ./web/next-app
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio-data:/data

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma-data:/chroma/chroma

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper

volumes:
  minio-data:
  chroma-data:
```

### Local Kubernetes (Optional)

For developers wanting to test Kubernetes deployment:

**Tools**: Kind or Minikube

**Manifests**:
- Namespace: `astraflow-lite`
- Deployments for each microservice
- Services for internal communication
- Ingress for external access
- PersistentVolumeClaims for data

## Security Considerations

### Authentication
- JWT tokens with 24-hour expiration
- Refresh token mechanism
- Password hashing with bcrypt

### Authorization
- Row-level security: Users can only access their own Collections
- API key management for LLM providers (environment variables)
- MinIO presigned URLs with 1-hour expiration

### Data Protection
- SQLite database file permissions (600)
- Vector store access restricted to internal network
- No sensitive data in logs

### API Security
- Rate limiting per user (100 requests/minute)
- Request size limits (10MB for uploads)
- CORS configuration for frontend origin only

## Monitoring and Observability

### Metrics (Prometheus)

```python
# Request metrics
http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
http_request_duration_seconds = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Task metrics
celery_task_duration_seconds = Histogram('celery_task_duration_seconds', 'Task duration', ['task_name'])
celery_task_failures_total = Counter('celery_task_failures_total', 'Task failures', ['task_name'])

# LLM metrics
llm_api_calls_total = Counter('llm_api_calls_total', 'LLM API calls', ['provider', 'model'])
llm_tokens_used_total = Counter('llm_tokens_used_total', 'Tokens used', ['provider', 'model'])
llm_cost_dollars_total = Counter('llm_cost_dollars_total', 'Estimated cost', ['provider', 'model'])

# Vector store metrics
vector_search_duration_seconds = Histogram('vector_search_duration_seconds', 'Vector search duration')
vector_upsert_duration_seconds = Histogram('vector_upsert_duration_seconds', 'Vector upsert duration')
```

### Logging

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for recoverable issues
- ERROR: Error messages for failures
- CRITICAL: Critical issues requiring immediate attention

**Log Format:**
```json
{
  "timestamp": "2024-12-08T10:30:00Z",
  "level": "INFO",
  "service": "api-gateway",
  "request_id": "req_abc123",
  "user_id": "user_xyz",
  "message": "Collection created",
  "collection_id": "c1",
  "duration_ms": 45
}
```

### Dashboards (Grafana)

1. **System Overview**: Request rates, error rates, latencies
2. **Task Queue**: Queue depth, task duration, failure rate
3. **LLM Usage**: API calls, tokens, costs by provider
4. **Stock Pipeline**: Tick rate, indicator computation time
5. **Storage**: Database size, vector count, MinIO usage

## Future Enhancements

1. **Additional LLM Providers**: Anthropic Claude, Cohere, local models
2. **Advanced RAG**: Hybrid search, reranking, query expansion
3. **Workflow Marketplace**: Share and discover workflows
4. **Real-time Collaboration**: Multi-user document annotation
5. **Advanced Stock Analysis**: ML-based predictions, alerts
6. **Cloud Deployment**: Kubernetes manifests for cloud providers
7. **Mobile App**: React Native frontend
8. **Plugin System**: Custom node types for workflows
