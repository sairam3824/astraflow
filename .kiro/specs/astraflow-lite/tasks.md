# Implementation Plan

- [x] 1. Set up project structure and shared libraries
  - Create monorepo directory structure with services, web, libs, and infra folders
  - Initialize shared Pydantic schemas library (Collection, Document, Chunk, Vector, Workflow, GitHubRepository, ChatSession, ChatMessage)
  - Set up shared utilities for logging (structured JSON), metrics (Prometheus), and configuration
  - Create .env.example with required environment variables
  - _Requirements: 16.1_

- [x] 2. Set up local infrastructure with Docker Compose
  - Create docker-compose.yml with SQLite volume, Redis, MinIO, ChromaDB, Kafka, and Zookeeper
  - Configure service networking and port mappings
  - Add health checks for all infrastructure services
  - Create initialization scripts for MinIO buckets and ChromaDB collections
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 3. Implement API Gateway with authentication
  - Create FastAPI application with JWT authentication middleware
  - Implement user registration and login endpoints (POST /auth/register, POST /auth/login)
  - Set up SQLite connection and User table schema
  - Implement JWT token generation and validation
  - Add request logging and Prometheus metrics middleware
  - _Requirements: 10.1, 10.5_

- [x] 4. Implement Collection management endpoints
  - Create Collection CRUD endpoints (POST /collections, GET /collections, DELETE /collections/{id})
  - Implement Collection table in SQLite with unique constraint on (owner_id, name)
  - Add Collection ownership validation middleware
  - Initialize empty ChromaDB collection when Collection is created
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 10.2, 10.3, 10.4_

- [x] 5. Implement document upload and storage
  - Create MinIO client wrapper for presigned URL generation
  - Implement upload endpoint (POST /collections/{id}/upload) that returns presigned URL
  - Create Document table in SQLite with foreign key to Collections
  - Implement document metadata storage after upload completion
  - _Requirements: 2.1, 2.2_

- [x] 6. Implement Ingestion Service
  - Create Ingestion Service with FastAPI endpoints
  - Implement PDF text extraction using pdfminer.six
  - Add OCR support using Tesseract for scanned documents
  - Implement semantic chunking algorithm with configurable token limits and overlap
  - Create Chunk table in SQLite with foreign key to Documents
  - Store chunks in SQLite with text, token count, and offset
  - _Requirements: 2.3, 2.4, 2.5_

- [x] 7. Set up Celery task manager
  - Create Celery application with Redis broker and result backend
  - Configure task retry policies with exponential backoff
  - Implement task types: ingest_document_task, embed_chunks_task, summarize_document_task, run_workflow_task, analyze_github_repo_task
  - Add Celery worker Dockerfile and service to docker-compose
  - Set up Celery Beat for scheduled tasks (optional)
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 8. Implement Embedding Service
  - Create Embedding Service with OpenAI embedding API client
  - Implement ChromaDB client wrapper for vector upsert and search
  - Create embed_chunks Celery task that processes chunks and upserts to ChromaDB
  - Add vector metadata (chunk_id, collection_id) to ChromaDB records
  - Update Document status to "ingested" after all chunks are embedded
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 9. Implement ingestion workflow endpoint
  - Create POST /collections/{id}/ingest endpoint in API Gateway
  - Trigger ingest_document_task Celery task asynchronously
  - Return job ID for status tracking
  - Chain ingestion → embedding tasks in Celery
  - _Requirements: 2.3, 3.1_

- [x] 10. Implement Model Adapter layer
  - Create abstract ModelAdapter base class with complete() and estimate_cost() methods
  - Implement OpenAIAdapter for GPT models with streaming support
  - Implement GeminiAdapter for Gemini models with streaming support
  - Add API key configuration from environment variables
  - Implement token counting and cost estimation logic
  - Add logging for all LLM API calls with tokens and cost
  - _Requirements: 14.4, 14.5, 12.4_

- [x] 11. Implement Model Router
  - Create ModelRouter class with select_model() method
  - Implement explicit model selection (user preference)
  - Implement automatic routing based on task classification (summarization → Gemini, large context → GPT-4, default → GPT-3.5)
  - Add routing policy configuration (cost, speed, accuracy)
  - _Requirements: 14.1, 14.2, 14.3, 4.3_

- [x] 12. Implement Agent Router Service for RAG
  - Create Agent Router Service with FastAPI endpoints
  - Implement RAG search endpoint (GET /collections/{id}/search)
  - Add vector retrieval from ChromaDB with top-k parameter
  - Implement prompt construction combining query, retrieved chunks, and system instructions
  - Integrate Model Router for LLM selection
  - Call Model Adapter to generate response
  - Return search results with chunks and optional AI answer
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 13. Implement chat session management
  - Create ChatSession and ChatMessage tables in SQLite
  - Implement chat session endpoints (POST /chat/sessions, POST /chat/sessions/{id}/messages)
  - Store chat messages with role (user/assistant), content, and tokens
  - Add optional Collection association for context-aware chat
  - Implement chat history retrieval
  - _Requirements: 5.1, 5.2_

- [x] 14. Implement chat with RAG and streaming
  - Add Collection-aware retrieval in chat message handler
  - Integrate Model Router for chat responses
  - Implement SSE endpoint (GET /chat/sessions/{id}/stream) for streaming responses
  - Store assistant responses in chat history after streaming completes
  - _Requirements: 5.3, 5.4, 5.5_

- [x] 15. Implement document summarization
  - Create Summary table in SQLite with foreign key to Documents
  - Implement summarize_document Celery task using Gemini adapter
  - Trigger summarization task after PDF ingestion completes
  - Store summary in SQLite associated with Document
  - Implement summary regeneration endpoint (POST /summaries/{doc_id}/regenerate)
  - Add optional n8n webhook endpoint for scheduled summarization
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 16. Implement Workflow Runner Service
  - Create Workflow table in SQLite for storing LangGraph JSON definitions
  - Implement workflow CRUD endpoints (POST /workflows, GET /workflows, POST /workflows/{id}/run)
  - Integrate LangChain and LangGraph for workflow orchestration
  - Implement workflow node types: retrieve (query vector store), llm (call model), postprocess (extract entities), notify (placeholder)
  - Add workflow validation before execution
  - Execute workflows asynchronously via Celery task
  - Return workflow execution results and update status
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 17. Implement Stock Producer Service
  - Create Stock Producer Service with Kafka producer client
  - Implement simulated stock data generator (or real feed connector)
  - Publish tick records to Kafka topic "market.ticks" partitioned by symbol
  - Add tick schema (symbol, price, volume, timestamp)
  - _Requirements: 8.1_

- [x] 18. Implement Stock Analysis Service
  - Create Stock Analysis Service with Kafka consumer
  - Consume from "market.ticks" topic
  - Implement indicator calculations (SMA, EMA, VWAP, volatility) using pandas and numpy
  - Publish computed indicators to "market.indicators" topic
  - Store latest indicators in Redis with symbol as key
  - _Requirements: 8.2, 8.3_

- [x] 19. Implement stock indicators API endpoint
  - Create GET /stocks/{symbol}/indicators endpoint in API Gateway
  - Retrieve latest indicators from Redis
  - Return indicator values (SMA, EMA, VWAP, volatility) as JSON
  - _Requirements: 8.4_

- [x] 20. Implement GitHub Analysis Service
  - Create GitHub Analysis Service with FastAPI endpoints
  - Implement repository cloning using GitPython (shallow clone)
  - Analyze codebase structure: detect languages, frameworks, file types
  - Extract dependencies from package files (package.json, requirements.txt, etc.)
  - Create GitHubAnalysis table in SQLite
  - _Requirements: 15.1, 15.2_

- [x] 21. Implement README generation for GitHub repositories
  - Create README generation prompt template with repository structure and dependencies
  - Use Model Router to select GPT or Gemini for generation
  - Generate README with sections: description, installation, usage, contribution guidelines
  - Validate generated README contains required sections
  - Store README content in GitHubAnalysis table
  - _Requirements: 15.3, 15.4_

- [x] 22. Implement license recommendation for GitHub repositories
  - Analyze project characteristics (language, dependencies, existing license)
  - Implement license recommendation logic based on project type
  - Generate license recommendation using LLM if needed
  - Store license recommendation in GitHubAnalysis table
  - _Requirements: 15.5_

- [x] 23. Implement GitHub analysis endpoints
  - Create POST /github/analyze endpoint to trigger analysis
  - Create GET /github/analysis/{id} endpoint to retrieve results
  - Trigger analyze_github_repo Celery task asynchronously
  - Return analysis ID for status tracking
  - _Requirements: 15.6_

- [x] 24. Implement structured logging across all services
  - Add JSON logging formatter to all microservices
  - Include required fields: timestamp, level, service, request_id, user_id, message
  - Log all operations with appropriate log levels
  - Add task failure logging with stack traces and parameters
  - _Requirements: 12.1, 12.5_

- [x] 25. Implement Prometheus metrics
  - Add Prometheus client to all services
  - Expose metrics endpoints (/metrics) on all services
  - Implement key metrics: http_requests_total, http_request_duration_seconds, celery_task_duration_seconds, llm_api_calls_total, llm_tokens_used_total, vector_search_duration_seconds
  - Add Prometheus service to docker-compose
  - _Requirements: 12.2_

- [x] 26. Implement error handling and validation
  - Add global exception handlers to API Gateway
  - Implement consistent error response format with error codes and details
  - Add Pydantic validation error handlers with detailed field messages
  - Implement retry logic for external API calls with exponential backoff
  - Add circuit breaker for repeated LLM API failures
  - _Requirements: 16.2, 16.4_

- [x] 27. Implement Frontend - Dashboard page
  - Create Next.js application with TailwindCSS
  - Implement dashboard page (/) displaying Collections list, recent documents, and system status
  - Add API client wrapper for backend communication
  - Implement authentication flow (login/register forms)
  - _Requirements: 13.1_

- [x] 28. Implement Frontend - Collection detail page
  - Create Collection detail page (/collections/[id])
  - Implement document upload form with presigned URL handling
  - Display document list with status and summaries
  - Add RAG search interface with query input and results display
  - _Requirements: 13.2_

- [x] 29. Implement Frontend - Chat interface
  - Create chat page (/chat/[session])
  - Implement model selection dropdown (GPT/Gemini)
  - Add Collection association selector for context-aware chat
  - Display message history with user/assistant roles
  - Implement streaming response handling with SSE
  - _Requirements: 13.3_

- [x] 30. Implement Frontend - Workflow editor
  - Create workflow editor page (/workflows)
  - Implement visual workflow builder for LangGraph JSON
  - Add node palette (retrieve, llm, postprocess, notify)
  - Implement workflow execution trigger and results display
  - _Requirements: 13.4_

- [x] 31. Implement Frontend - Stock page
  - Create stock page (/stocks)
  - Implement symbol selector
  - Add real-time chart display using Chart.js or Recharts
  - Display computed indicators (SMA, EMA, VWAP, volatility)
  - Implement WebSocket or polling for real-time updates
  - _Requirements: 13.5_

- [x] 32. Implement Frontend - GitHub analysis page
  - Create GitHub analysis page (/github)
  - Add repository URL input form
  - Display analysis status and progress
  - Show generated README with syntax highlighting
  - Display license recommendation
  - Add download buttons for README and license files
  - _Requirements: 15.6_

- [x] 33. Add Grafana dashboards
  - Add Grafana service to docker-compose
  - Create dashboard for system overview (request rates, error rates, latencies)
  - Create dashboard for task queue (queue depth, task duration, failure rate)
  - Create dashboard for LLM usage (API calls, tokens, costs by provider)
  - Create dashboard for stock pipeline (tick rate, indicator computation time)
  - _Requirements: 12.3_

- [x] 34. Create documentation and setup scripts
  - Write README.md with project overview and setup instructions
  - Create architecture.md with detailed system architecture diagrams
  - Write runbook.md with operational procedures
  - Create setup-dev.sh script for initial environment setup
  - Add seed-sample-data.py script for demo data
  - Document API endpoints with OpenAPI/Swagger
  - _Requirements: All_

- [x] 35. Final checkpoint - Verify implementation
  - Verify all services are running correctly, ask the user if questions arise.
