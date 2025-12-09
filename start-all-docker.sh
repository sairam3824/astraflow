#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AstraFlow Lite (Full Docker Mode)...${NC}"

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

# Build and start all services
echo -e "${GREEN}Building and starting all services...${NC}"
docker-compose up -d --build

# Wait for infrastructure services to be ready
echo -e "${YELLOW}Waiting for infrastructure services to be ready (30s)...${NC}"
sleep 30

# Initialize MinIO
echo -e "${GREEN}Initializing MinIO buckets...${NC}"
chmod +x infra/init-minio.sh
./infra/init-minio.sh || echo -e "${YELLOW}MinIO initialization skipped${NC}"

# Wait for application services to start
echo -e "${YELLOW}Waiting for application services to start (15s)...${NC}"
sleep 15

echo ""
echo -e "${GREEN}✓ AstraFlow Lite is running in full Docker mode!${NC}"
echo ""
echo "Access points:"
echo "  Frontend:      http://localhost:8080"
echo "  API Gateway:   http://localhost:8080"
echo "  Ingestion:     http://localhost:8001"
echo "  Embedding:     http://localhost:8002"
echo "  Agent Router:  http://localhost:8003"
echo "  Workflow:      http://localhost:8004"
echo "  Stock Prod:    http://localhost:8005"
echo "  Stock Anal:    http://localhost:8006"
echo "  GitHub Anal:   http://localhost:8007"
echo "  Prometheus:    http://localhost:9090"
echo "  Grafana:       http://localhost:3001 (admin/admin)"
echo "  MinIO Console: http://localhost:9001 (minioadmin/minioadmin)"
echo "  ChromaDB:      http://localhost:8000"
echo ""
echo "View logs with: docker-compose logs -f [service_name]"
echo "View all services: docker-compose ps"
echo ""
echo "To stop all services, run: docker-compose down"
echo ""
