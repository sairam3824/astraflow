#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "AstraFlow Docker Setup Verification"
echo "=========================================="
echo ""

# Check Docker
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Installed${NC}"
    docker --version
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo ""

# Check Docker Compose
echo -n "Checking Docker Compose... "
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Installed${NC}"
    docker-compose --version
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo ""

# Check if Docker daemon is running
echo -n "Checking Docker daemon... "
if docker info &> /dev/null; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not running${NC}"
    echo "Please start Docker daemon"
    exit 1
fi
echo ""

# Check .env file
echo -n "Checking .env file... "
if [ -f .env ]; then
    echo -e "${GREEN}✓ Found${NC}"
    
    # Check for required keys
    echo "Checking required environment variables:"
    
    if grep -q "OPENAI_API_KEY=your-openai-api-key" .env; then
        echo -e "  ${YELLOW}⚠ OPENAI_API_KEY not set${NC}"
    else
        echo -e "  ${GREEN}✓ OPENAI_API_KEY set${NC}"
    fi
    
    if grep -q "GEMINI_API_KEY=your-gemini-api-key" .env; then
        echo -e "  ${YELLOW}⚠ GEMINI_API_KEY not set${NC}"
    else
        echo -e "  ${GREEN}✓ GEMINI_API_KEY set${NC}"
    fi
    
    if grep -q "JWT_SECRET=your-secret-key-change-in-production" .env; then
        echo -e "  ${YELLOW}⚠ JWT_SECRET using default (change for production)${NC}"
    else
        echo -e "  ${GREEN}✓ JWT_SECRET customized${NC}"
    fi
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Run: cp .env.example .env"
    exit 1
fi
echo ""

# Check if services are running
echo "Checking running services:"
if docker-compose ps | grep -q "Up"; then
    docker-compose ps
    echo ""
    echo -e "${GREEN}✓ Services are running${NC}"
else
    echo -e "${YELLOW}⚠ No services running${NC}"
    echo "Run: ./start-all-docker.sh"
fi
echo ""

# Check ports
echo "Checking port availability:"
PORTS=(8080 8001 8002 8003 8004 8005 8006 8007 6379 9000 9001 8000 9092 2181 9090 3001)
PORT_NAMES=("API Gateway" "Ingestion" "Embedding" "Agent Router" "Workflow" "Stock Prod" "Stock Anal" "GitHub Anal" "Redis" "MinIO" "MinIO Console" "ChromaDB" "Kafka" "Zookeeper" "Prometheus" "Grafana")

for i in "${!PORTS[@]}"; do
    PORT=${PORTS[$i]}
    NAME=${PORT_NAMES[$i]}
    
    if netstat -an 2>/dev/null | grep -q ":$PORT "; then
        echo -e "  ${GREEN}✓${NC} Port $PORT ($NAME) - In use"
    else
        echo -e "  ${YELLOW}○${NC} Port $PORT ($NAME) - Available"
    fi
done
echo ""

# Summary
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. If services are not running: ./start-all-docker.sh"
echo "2. Access frontend: http://localhost:8080"
echo "3. View logs: docker-compose logs -f"
echo "4. Check status: docker-compose ps"
echo ""
