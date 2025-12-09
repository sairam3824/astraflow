#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AstraFlow Lite...${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env and add your API keys, then run this script again.${NC}"
    exit 1
fi

# Create data directory
mkdir -p data

# Create logs directory
mkdir -p logs

# Start Docker infrastructure
echo -e "${GREEN}Starting Docker infrastructure...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}Waiting for infrastructure services to be ready (30s)...${NC}"
sleep 30

# Initialize MinIO
echo -e "${GREEN}Initializing MinIO buckets...${NC}"
chmod +x infra/init-minio.sh
./infra/init-minio.sh || echo -e "${YELLOW}MinIO initialization skipped${NC}"

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
fi

# Start backend services in background
echo -e "${GREEN}Starting backend services...${NC}"

echo "Starting API Gateway..."
python -m services.api_gateway.main > logs/api_gateway.log 2>&1 &
echo $! > logs/api_gateway.pid

echo "Starting Ingestion Service..."
python -m services.ingestion.main > logs/ingestion.log 2>&1 &
echo $! > logs/ingestion.pid

echo "Starting Embedding Service..."
python -m services.embedding.main > logs/embedding.log 2>&1 &
echo $! > logs/embedding.pid

echo "Starting Agent Router..."
python -m services.agent_router.main > logs/agent_router.log 2>&1 &
echo $! > logs/agent_router.pid

echo "Starting Chat Service..."
python -m services.chat_service.main > logs/chat_service.log 2>&1 &
echo $! > logs/chat_service.pid

echo "Starting Workflow Runner..."
python -m services.workflow_runner.main > logs/workflow_runner.log 2>&1 &
echo $! > logs/workflow_runner.pid

echo "Starting Stock Producer..."
python -m services.stock_producer.main > logs/stock_producer.log 2>&1 &
echo $! > logs/stock_producer.pid

echo "Starting Stock Analysis..."
python -m services.stock_analysis.main > logs/stock_analysis.log 2>&1 &
echo $! > logs/stock_analysis.pid

echo "Starting GitHub Analysis..."
python -m services.github_analysis.main > logs/github_analysis.log 2>&1 &
echo $! > logs/github_analysis.pid

echo "Starting Celery Worker..."
celery -A services.celery_worker.celery_app worker --loglevel=info > logs/celery.log 2>&1 &
echo $! > logs/celery.pid

# Wait a bit for backend to start
sleep 5

echo ""
echo -e "${GREEN}✓ AstraFlow Lite is starting up!${NC}"
echo ""
echo "Access points:"
echo "  Frontend:      http://localhost:8080"
echo "  API Gateway:   http://localhost:8080"
echo "  Prometheus:    http://localhost:9090"
echo "  Grafana:       http://localhost:3001 (admin/admin)"
echo "  MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"
echo "  ChromaDB:      http://localhost:8000"
echo ""
echo "Logs are available in the logs/ directory"
echo ""
echo "To stop all services, run: ./stop-all.sh"
echo ""
