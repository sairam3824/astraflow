#!/bin/bash
set -e

echo "Starting AstraFlow Lite in local development mode..."
echo "Note: This skips Docker services. You'll need to install and run them manually if needed."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
    exit 1
fi

# Create data directory
mkdir -p data

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To start services manually:"
echo ""
echo "1. API Gateway:"
echo "   python -m services.api_gateway.main"
echo ""
echo "2. Other services (in separate terminals):"
echo "   python -m services.ingestion.main"
echo "   python -m services.embedding.main"
echo "   python -m services.agent_router.main"
echo "   python -m services.workflow_runner.main"
echo "   python -m services.stock_producer.main"
echo "   python -m services.stock_analysis.main"
echo "   python -m services.github_analysis.main"
echo ""
echo "3. Celery worker:"
echo "   celery -A services.celery_worker.celery_app worker --loglevel=info"
echo ""
echo "4. Frontend:"
echo "   cd web && npm install && npm run dev"
echo ""
echo "Note: For full functionality, you'll need:"
echo "- Redis (brew install redis && redis-server)"
echo "- MinIO (brew install minio && minio server ./minio-data)"
echo "- ChromaDB (pip install chromadb && chroma run)"
echo "- Kafka (brew install kafka && kafka-server-start)"
