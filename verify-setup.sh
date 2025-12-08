#!/bin/bash

echo "Verifying AstraFlow Lite setup..."
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✓ .env file exists"
else
    echo "✗ .env file missing"
fi

# Check Docker services
echo ""
echo "Checking Docker services..."
docker-compose ps

# Check if data directory exists
if [ -d data ]; then
    echo "✓ Data directory exists"
else
    echo "✗ Data directory missing"
fi

# Check Python dependencies
echo ""
echo "Checking Python environment..."
python3 -c "import fastapi, celery, chromadb, openai" 2>/dev/null && echo "✓ Core Python packages installed" || echo "✗ Some Python packages missing"

# Check frontend
if [ -d web/node_modules ]; then
    echo "✓ Frontend dependencies installed"
else
    echo "✗ Frontend dependencies missing"
fi

echo ""
echo "Verification complete!"
echo ""
echo "If all checks passed, you can start the services."
echo "If any checks failed, run ./setup-dev.sh to fix issues."
