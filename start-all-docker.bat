@echo off
echo Starting AstraFlow Lite (Full Docker Mode)...

REM Check if .env exists
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit .env and add your API keys, then run this script again.
    exit /b 1
)

REM Create directories
if not exist data mkdir data
if not exist logs mkdir logs

REM Build and start all services
echo Building and starting all services...
docker-compose up -d --build

REM Wait for services
echo Waiting for services to be ready...
timeout /t 45 /nobreak

echo.
echo AstraFlow Lite is running in full Docker mode!
echo.
echo Access points:
echo   Frontend:      http://localhost:8080
echo   API Gateway:   http://localhost:8080
echo   Ingestion:     http://localhost:8001
echo   Embedding:     http://localhost:8002
echo   Agent Router:  http://localhost:8003
echo   Workflow:      http://localhost:8004
echo   Stock Prod:    http://localhost:8005
echo   Stock Anal:    http://localhost:8006
echo   GitHub Anal:   http://localhost:8007
echo   Prometheus:    http://localhost:9090
echo   Grafana:       http://localhost:3001 (admin/admin)
echo   MinIO Console: http://localhost:9001 (minioadmin/minioadmin)
echo   ChromaDB:      http://localhost:8000
echo.
echo View logs with: docker-compose logs -f [service_name]
echo View all services: docker-compose ps
echo.
echo To stop all services, run: docker-compose down
echo.
