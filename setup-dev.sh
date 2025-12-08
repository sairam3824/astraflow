#!/bin/bash
set -e

echo "Setting up AstraFlow Lite development environment..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
fi

# Create data directory
mkdir -p data

# Start infrastructure
echo "Starting infrastructure services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize MinIO
echo "Initializing MinIO buckets..."
chmod +x infra/init-minio.sh
./infra/init-minio.sh || echo "MinIO initialization skipped (may need manual setup)"

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd web
npm install
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "To start the services:"
echo "1. Backend: python -m services.api_gateway.main (and other services)"
echo "2. Celery: celery -A services.celery_worker.celery_app worker --loglevel=info"
echo "3. Frontend: cd web && npm run dev"
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- API: http://localhost:8000"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3001"
