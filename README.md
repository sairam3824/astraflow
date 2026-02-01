# AstraFlow 🚀

AstraFlow is a comprehensive **AI-Powered Intelligence Platform** designed to streamline workflows, analyze data, and provide intelligent search capabilities. It combines modern RAG (Retrieval-Augmented Generation) architectures, real-time data streaming, and autonomous agents into a unified, premium user interface.

## ✨ Key Features

### 1. **Intelligent Knowledge Base (RAG)** 🧠
*   **Semantic Search**: Upload PDF/Text documents and perform complex queries using AI.
*   **Vector Search**: Powered by ChromaDB for high-performance similarity search.
*   **Document Management**: Organize knowledge into collections with tracking of indexing status.
*   **Contextual Chat**: Chat with specific collections using an intelligent agent.

### 2. **Real-Time Market Intelligence** 📈
*   **Live Stock Data**: Real-time stock price streaming via **Kafka** & **WebSockets**.
*   **Technical Analysis**: Automated calculation of indicators (SMA, EMA, RSI) on the fly.
*   **Interactive Charts**: Beautiful, glassmorphism-styled charts using Chart.js.

### 3. **Workflow Automation** ⚙️
*   **Visual Workflow Builder**: Create implementation plans and task sequences.
*   **Autonomous Agents**: `agent_router` orchestrates complex multi-step tasks.
*   **Task Execution**: Background processing powered by **Celery** and **Redis**.

### 4. **Developer Tools** 🛠️
*   **GitHub Docs Generator**: Auto-generate `README.md` and `LICENSE` files for your repositories.
*   **Code Analysis**: Deep dive into codebases with AI-assisted insights.

### 5. **Premium UI/UX** 🎨
*   **Modern Design**: Glassmorphism, tailored gradients, and smooth animations.
*   **Dark Mode**: A professional, dark-themed sidebar and polished interface elements.
*   **Responsive**: Optimized for various screen sizes.

---

## 🏗️ Architecture

AstraFlow is built as a **Microservices** application, containerized with Docker.

| Service | Port | Description |
| :--- | :--- | :--- |
| **API Gateway** | `8080` | Main entry point, serves UI, Authentication, and routes requests. |
| **Ingestion** | `8001` | Handles document upload and text chunking. |
| **Embedding** | `8002` | Generates vector embeddings for documents. |
| **Agent Router** | `8003` | Orchestrates AI agent interactions. |
| **Workflow Runner** | `8004` | Executes automated workflows. |
| **Stock Producer** | `8005` | Fetches and streams stock data to Kafka. |
| **Stock Analysis** | `8006` | Consumes Kafka streams and performs technical analysis. |
| **GitHub Analysis** | `8007` | specialized service for GitHub API interactions. |

### Infrastructure Stack
*   **Database**: SQLite (App Data), ChromaDB (Vectors).
*   **Messaging**: Apache Kafka (Real-time), Redis (Queues/Cache).
*   **Storage**: MinIO (S3-compatible object storage).
*   **Monitoring**: Prometheus & Grafana.

---

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.9+ (for local development)

### Quick Start (Docker)

The easiest way to run the full platform is via Docker Compose.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/sairam3824/astraflow.git
    cd astraflow
    ```

2.  **Set up Environment Variables**:
    Copy `.env.example` to `.env` and add your API keys (OpenAI/Gemini).
    ```bash
    cp .env.example .env
    ```

3.  **Start Services**:
    Use the provided script to start everything:
    ```bash
    ./start-all.sh
    ```
    *Or manually:* `docker-compose up --build -d`

4.  **Access the Platform**:
    Open your browser and navigate to:
    **[http://localhost:8080](http://localhost:8080)**

---

## 💻 Local Development

If you want to run services individually without Docker (e.g., for debugging):

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start Infrastructure** (Redis, Kafka, MinIO, etc. are still required):
    ```bash
    docker-compose -f docker-compose.yml up -d redis minio chromadb kafka zookeeper
    ```

3.  **Run API Gateway**:
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    python -m services.api_gateway.main
    ```

---

## 📂 Project Structure

```
astraflow/
├── services/               # Microservices source code
│   ├── api_gateway/        # Main API & UI serving
│   ├── ingestion/          # Document processing
│   ├── embedding/          # Vector embeddings
│   ├── stock_analysis/     # Financial data processing
│   └── ...
├── templates/              # HTML Frontend Templates
├── infra/                  # Infrastructure config (Prometheus, Grafana)
├── data/                   # Persistent data storage
├── tests/                  # Integration tests
└── docker-compose.yml      # Container orchestration
```

## 🔐 Credentials
*   **Default Login**: Register a new account on the login page.
*   **MinIO Console**: `http://localhost:9001` (User: `minioadmin`, Pass: `minioadmin`)
*   **Grafana**: `http://localhost:3001` (User: `admin`, Pass: `admin`)

---

<p align="center">
  Built with ❤️ by the AstraFlow Team
</p>
