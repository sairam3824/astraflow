# Requirements Document

## Introduction

AstraFlow Lite is a developer-friendly, modular AI platform designed to run entirely locally via Docker Compose or Kubernetes. The system enables users to create document collections, perform RAG (Retrieval-Augmented Generation) queries, engage in multi-model chat sessions, design custom workflows, automatically summarize documents, analyze real-time stock data, and generate documentation for GitHub repositories. The platform integrates AI providers (OpenAI GPT and Google Gemini initially) and uses local databases: ChromaDB or FAISS for vector embeddings, SQLite for metadata storage, Kafka for stock data streaming, and Celery for background task orchestration.

## Glossary

- **AstraFlow System**: The complete local AI platform including all microservices and components
- **Collection**: A named dataset containing related documents (e.g., "Legal", "Finance")
- **RAG (Retrieval-Augmented Generation)**: A technique combining document retrieval with LLM generation
- **Vector Index**: A searchable index of document embeddings stored per Collection
- **LLM Provider**: External API services for language models (initially OpenAI GPT and Google Gemini)
- **Model Router**: Component that selects appropriate LLM based on task or user preference (initially between GPT and Gemini)
- **Workflow**: A sequence of processing steps defined using LangChain/LangGraph
- **Chunk**: A semantically meaningful segment of a document with associated metadata
- **Embedding Service**: Service that converts text chunks into vector representations
- **Ingestion Service**: Service that processes uploaded documents into chunks
- **API Gateway**: Single entry point for all client requests with authentication
- **Celery Worker**: Background task processor for asynchronous operations
- **Kafka Cluster**: Event streaming platform used exclusively for stock data
- **Stock Tick**: Real-time market data point for a stock symbol
- **Indicator**: Computed metric (SMA, EMA, VWAP, volatility) derived from stock data
- **n8n**: Optional workflow automation tool for scheduling tasks
- **MinIO**: S3-compatible object storage for document files
- **ChromaDB**: Local vector database option for storing embeddings
- **FAISS**: Alternative local vector database option for storing embeddings
- **SQLite**: Local relational database for storing document metadata, Collections, and system data
- **GitHub Repository**: A remote code repository that can be analyzed for documentation generation

## Requirements

### Requirement 1

**User Story:** As a user, I want to create and manage Collections, so that I can organize documents into logical datasets for different domains or projects.

#### Acceptance Criteria

1. WHEN a user creates a Collection with a name and optional domain THEN the AstraFlow System SHALL create a new Collection record with unique identifier and timestamp
2. WHEN a user requests a list of Collections THEN the AstraFlow System SHALL return all Collections owned by that user with metadata
3. WHEN a user deletes a Collection THEN the AstraFlow System SHALL remove the Collection record, associated documents, chunks, and vector indices
4. THE AstraFlow System SHALL enforce unique Collection names per user
5. WHEN a Collection is created THEN the AstraFlow System SHALL initialize an empty vector index for that Collection

### Requirement 2

**User Story:** As a user, I want to upload documents to a Collection, so that I can build a knowledge base for RAG queries and analysis.

#### Acceptance Criteria

1. WHEN a user requests to upload a document to a Collection THEN the AstraFlow System SHALL generate a presigned URL for secure upload to MinIO
2. WHEN a document upload completes THEN the AstraFlow System SHALL create a Document record with filename, page count, and pending status
3. WHEN a user triggers ingestion for an uploaded document THEN the Ingestion Service SHALL extract text content from the document
4. IF a document contains images or scanned content THEN the Ingestion Service SHALL apply OCR using Tesseract to extract text
5. WHEN text extraction completes THEN the Ingestion Service SHALL perform semantic chunking to create Chunk records with text, token count, and offset metadata

### Requirement 3

**User Story:** As a user, I want documents to be automatically embedded and indexed, so that I can perform semantic search and RAG queries on my Collections.

#### Acceptance Criteria

1. WHEN document chunking completes THEN the AstraFlow System SHALL trigger the Embedding Service to process all chunks
2. WHEN the Embedding Service processes chunks THEN the Embedding Service SHALL call the embedding provider API to generate vector representations
3. WHEN embeddings are generated THEN the Embedding Service SHALL upsert vectors into the Collection-specific vector index in Chroma or FAISS
4. THE Embedding Service SHALL associate each vector with its corresponding chunk identifier and Collection identifier
5. WHEN all chunks are embedded THEN the AstraFlow System SHALL update the Document status to ingested

### Requirement 4

**User Story:** As a user, I want to perform RAG searches on my Collections, so that I can retrieve relevant information and get AI-generated answers based on my documents.

#### Acceptance Criteria

1. WHEN a user submits a search query for a Collection THEN the AstraFlow System SHALL retrieve the top-k most similar chunks from that Collection vector index
2. WHEN retrieval completes and a model is specified THEN the Agent Service SHALL construct a prompt combining the query, retrieved chunks, and system instructions
3. WHEN a prompt is constructed THEN the Model Router SHALL select an appropriate LLM Provider based on user preference or automatic routing policy
4. WHEN an LLM Provider is selected THEN the Model Adapter SHALL call the external API and return the generated response
5. THE AstraFlow System SHALL return search results containing retrieved chunks and optional AI-generated answer with citations

### Requirement 5

**User Story:** As a user, I want to create and participate in chat sessions with GPT or Gemini models, so that I can have conversations with AI while leveraging my document Collections.

#### Acceptance Criteria

1. WHEN a user creates a chat session THEN the AstraFlow System SHALL create a session record with optional model selection between GPT and Gemini and Collection association
2. WHEN a user sends a message in a chat session THEN the AstraFlow System SHALL store the message in the chat history
3. IF a chat session is associated with a Collection THEN the Agent Service SHALL retrieve relevant chunks from that Collection before generating a response
4. WHEN generating a chat response THEN the Model Router SHALL route the request to GPT or Gemini based on user selection or automatic task classification
5. WHEN a response is generated THEN the AstraFlow System SHALL stream the response to the client using SSE or WebSocket and store it in chat history

### Requirement 6

**User Story:** As a user, I want to design and execute custom workflows, so that I can automate complex multi-step AI processing pipelines.

#### Acceptance Criteria

1. WHEN a user creates a workflow THEN the AstraFlow System SHALL store the workflow definition as a LangGraph JSON structure with nodes and edges
2. THE AstraFlow System SHALL support workflow nodes including retrieve, llm, postprocess, and notify node types
3. WHEN a user executes a workflow THEN the Workflow Runner SHALL validate the workflow structure before execution
4. WHEN a workflow executes THEN the Workflow Runner SHALL process nodes in the defined order using LangChain and LangGraph orchestration
5. WHEN a workflow completes THEN the AstraFlow System SHALL return execution results and update workflow execution status

### Requirement 7

**User Story:** As a user, I want every uploaded PDF to be automatically summarized, so that I can quickly understand document contents without reading the full text.

#### Acceptance Criteria

1. WHEN a PDF document ingestion completes THEN the AstraFlow System SHALL trigger a Celery task to generate a summary
2. WHEN generating a summary THEN the Model Adapter SHALL call the Gemini API as the preferred provider with fallback to other providers
3. WHEN a summary is generated THEN the AstraFlow System SHALL create a Summary record associated with the Document
4. WHEN a user requests summary regeneration THEN the AstraFlow System SHALL create a new Celery task to regenerate the summary
5. WHERE n8n is configured THEN the AstraFlow System SHALL expose an endpoint for scheduled summary regeneration

### Requirement 8

**User Story:** As a user, I want to view real-time stock data with computed indicators, so that I can analyze market trends and make informed decisions.

#### Acceptance Criteria

1. WHEN the Stocks Producer receives market data THEN the Stocks Producer SHALL publish tick records to the Kafka topic partitioned by symbol
2. WHEN the Stock Analysis Service consumes tick records THEN the Stock Analysis Service SHALL compute technical indicators including SMA, EMA, VWAP, and volatility
3. WHEN indicators are computed THEN the Stock Analysis Service SHALL publish results to the indicators topic and store them in Redis
4. WHEN a user requests stock indicators for a symbol THEN the AstraFlow System SHALL return the latest computed indicators from Redis
5. THE Stock UI SHALL display real-time charts and indicator values updated as new data arrives

### Requirement 9

**User Story:** As a system administrator, I want all long-running and asynchronous operations to be handled by Celery workers, so that the system remains responsive and scalable.

#### Acceptance Criteria

1. THE AstraFlow System SHALL use Celery workers to execute document ingestion tasks asynchronously
2. THE AstraFlow System SHALL use Celery workers to execute embedding generation tasks asynchronously
3. THE AstraFlow System SHALL use Celery workers to execute summarization tasks asynchronously
4. THE AstraFlow System SHALL use Celery workers to execute workflow execution tasks asynchronously
5. WHEN a Celery task fails THEN the AstraFlow System SHALL retry the task with exponential backoff up to a configured maximum

### Requirement 10

**User Story:** As a user, I want to authenticate securely and have my data isolated, so that my Collections and documents remain private.

#### Acceptance Criteria

1. WHEN a user attempts to access the API Gateway THEN the API Gateway SHALL validate the JWT token for authentication
2. WHEN a user creates a Collection THEN the AstraFlow System SHALL associate the Collection with the authenticated user identifier
3. WHEN a user requests Collections THEN the AstraFlow System SHALL return only Collections owned by that user
4. WHEN a user attempts to access a Collection THEN the API Gateway SHALL verify the user has permission to access that Collection
5. THE API Gateway SHALL reject requests with invalid or expired JWT tokens with appropriate error responses

### Requirement 11

**User Story:** As a developer, I want the entire system to run locally using Docker Compose, so that I can develop and test without cloud dependencies.

#### Acceptance Criteria

1. THE AstraFlow System SHALL provide a docker-compose.yml file that defines all required services
2. WHEN a developer runs docker-compose up THEN the AstraFlow System SHALL start SQLite, Redis, MinIO, ChromaDB or FAISS, Kafka, Zookeeper, and all microservices
3. THE AstraFlow System SHALL configure service networking so that all microservices can communicate via Docker network
4. THE AstraFlow System SHALL expose the API Gateway and Frontend on accessible ports for local development
5. THE AstraFlow System SHALL persist data using Docker volumes for SQLite database file, MinIO, and vector databases

### Requirement 12

**User Story:** As a developer, I want comprehensive monitoring and logging, so that I can troubleshoot issues and understand system performance.

#### Acceptance Criteria

1. THE AstraFlow System SHALL emit structured JSON logs from all microservices
2. THE AstraFlow System SHALL expose Prometheus metrics for request latencies, queue depths, and task durations
3. WHEN Prometheus is configured THEN the AstraFlow System SHALL allow Grafana to visualize metrics with dashboards
4. THE AstraFlow System SHALL log all LLM API calls with token usage and approximate cost
5. WHEN a Celery task fails THEN the AstraFlow System SHALL log the failure with stack trace and task parameters

### Requirement 13

**User Story:** As a user, I want a modern web interface, so that I can interact with all platform features through an intuitive dashboard.

#### Acceptance Criteria

1. THE Frontend SHALL provide a dashboard page displaying Collections, recent documents, and system status
2. THE Frontend SHALL provide a Collection detail page with document upload, document list, and search interface
3. THE Frontend SHALL provide a chat interface with GPT or Gemini model selection, message history, and streaming responses
4. THE Frontend SHALL provide a workflow editor for creating and managing LangGraph workflows
5. THE Frontend SHALL provide a stock page displaying real-time charts and computed indicators for selected symbols

### Requirement 14

**User Story:** As a developer, I want the Model Router to intelligently select between GPT and Gemini, so that I can optimize for cost, speed, or accuracy based on task requirements.

#### Acceptance Criteria

1. WHEN a user explicitly selects GPT or Gemini THEN the Model Router SHALL use the specified LLM Provider
2. WHEN no model is specified THEN the Model Router SHALL classify the task type and select either GPT or Gemini
3. THE Model Router SHALL support routing policies based on task complexity, required speed, and cost constraints
4. THE Model Router SHALL maintain adapters for OpenAI GPT and Google Gemini with extensibility for future providers
5. WHEN a model call completes THEN the Model Adapter SHALL log token usage and estimated cost for tracking

### Requirement 15

**User Story:** As a developer, I want to analyze GitHub repositories and automatically generate README files and license recommendations, so that I can quickly document my projects.

#### Acceptance Criteria

1. WHEN a user provides a GitHub repository URL THEN the AstraFlow System SHALL clone or fetch the repository contents
2. WHEN repository contents are retrieved THEN the GitHub Analysis Service SHALL analyze the codebase structure, file types, and dependencies
3. WHEN analysis completes THEN the GitHub Analysis Service SHALL generate a comprehensive README file using GPT or Gemini
4. WHEN generating a README THEN the AstraFlow System SHALL include sections for project description, installation, usage, and contribution guidelines
5. WHEN analysis completes THEN the GitHub Analysis Service SHALL recommend appropriate open-source licenses based on project characteristics
6. THE AstraFlow System SHALL store the generated README and license recommendations for user review and download

### Requirement 16

**User Story:** As a developer, I want shared Pydantic schemas across all services, so that data validation and serialization remain consistent.

#### Acceptance Criteria

1. THE AstraFlow System SHALL define Collection, Document, Chunk, Vector, Workflow, and GitHubRepository schemas in a shared library
2. THE API Gateway SHALL validate all incoming requests against Pydantic schemas
3. THE microservices SHALL use shared schemas for inter-service communication
4. WHEN a schema validation fails THEN the AstraFlow System SHALL return a detailed error response with validation messages
5. THE AstraFlow System SHALL serialize all API responses using Pydantic models to ensure type safety
