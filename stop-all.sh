#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping AstraFlow Lite...${NC}"

# Stop all Python services
if [ -d "logs" ]; then
    for pidfile in logs/*.pid; do
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            service=$(basename "$pidfile" .pid)
            echo "Stopping $service (PID: $pid)..."
            kill $pid 2>/dev/null || echo "  Process already stopped"
            rm "$pidfile"
        fi
    done
fi

# Stop Docker services
echo -e "${YELLOW}Stopping Docker infrastructure...${NC}"
docker-compose down

echo -e "${GREEN}✓ All services stopped${NC}"
