# AstraFlow Lite

A locally-hosted AI platform with a beautiful modern dashboard for document management, RAG (Retrieval-Augmented Generation), multi-model chat, workflow automation, stock analysis, and GitHub repository documentation.

## 🚀 One-Command Start

```bash
./start-all.sh
```

Then open: **http://localhost:8000**

That's it! Everything runs automatically.

## Features

- **Document Collections**: Organize documents into logical datasets
- **RAG (Retrieval-Augmented Generation)**: Semantic search with AI-generated answers
- **Multi-Model Chat**: Chat with GPT or Gemini models with optional document context
- **Workflow Automation**: Design and execute custom AI workflows using LangGraph
- **Document Summarization**: Automatic PDF summarization
- **Stock Analysis**: Real-time stock data streaming with technical indicators
- **GitHub Analysis**: Automated README generation and license recommendations

## Architecture

AstraFlow Lite is built as a microservices architecture:

- **API Gateway**: Authentication and request routing
- **Ingestion Service**: PDF text extraction and chunking
- **Embedding Service**: Vector generation and ChromaDB storage
- **Agent Router**: RAG orchestration and LLM routing
- **Workflow Runner**: LangGraph workflow execution
- **Stock Services**: Kafka-based stock data pipeline
- **GitHub Analysis**: Repository analysis and documentation generation
- **Celery Workers**: Background task processing

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key (optional)
- Google Gemini API key (optional)

## Quick Start

### One-Command Setup

```bash
./start-all.sh
```

This single script will:
1. Check for `.env` file (creates from example if missing)
2. Start all Docker infrastructure services
3. Initialize MinIO buckets
4. Install dependencies if needed
5. Start all 8 backend microservices
6. Start the web dashboard

**First time?** The script will prompt you to add your API keys to `.env`, then run it again.

### Access the Application

Once started, open your browser to:

**🚀 Main Dashboard: http://localhost:8000**

Other services:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- MinIO Console: http://localhost:9001 (minioadmin/minioadmin)
- ChromaDB: http://localhost:8000

### Stop Everything

```bash
./stop-all.sh
```

## Using the Dashboard

1. **Register/Login** at http://localhost:8000/login
2. **Create Collections** to organize your documents
3. **Upload PDFs** to collections
4. **Search with RAG** - Ask questions about your documents
5. **Get AI Answers** powered by your document context

See [DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md) for detailed instructions.

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Collections
- `GET /collections` - List user's collections
- `POST /collections` - Create new collection
- `DELETE /collections/{id}` - Delete collection

### Documents
- `POST /collections/{id}/upload` - Get presigned URL for upload
- `POST /collections/{id}/ingest` - Trigger document ingestion

### Search
- `GET /collections/{id}/search` - Perform RAG search

### Chat
- `POST /chat/sessions` - Create chat session
- `POST /chat/sessions/{id}/messages` - Send message

### Workflows
- `POST /workflows` - Create workflow
- `POST /workflows/{id}/run` - Execute workflow

### Stocks
- `GET /stocks/{symbol}/indicators` - Get stock indicators

### GitHub
- `POST /github/analyze` - Analyze repository
- `GET /github/analysis/{id}` - Get analysis results

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

## Monitoring

- **Prometheus**: Metrics collection at http://localhost:9090
- **Grafana**: Visualization dashboards at http://localhost:3001
- **Logs**: Structured JSON logs from all services

## Development

### Project Structure
```
astraflow-lite/
├── services/           # Microservices
│   ├── api_gateway/
│   ├── ingestion/
│   ├── embedding/
│   ├── agent_router/
│   ├── workflow_runner/
│   ├── stock_producer/
│   ├── stock_analysis/
│   ├── github_analysis/
│   └── celery_worker/
├── libs/              # Shared libraries
│   ├── schemas/
│   ├── utils/
│   ├── model_adapter/
│   └── model_router/
├── web/               # Next.js frontend
├── infra/             # Infrastructure configs
└── docker-compose.yml
```

### Running Tests
```bash
pytest
```

## License

MIT
