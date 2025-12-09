@echo off
echo ==========================================
echo AstraFlow Docker Setup Verification
echo ==========================================
echo.

REM Check Docker
echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker is installed
    docker --version
) else (
    echo [ERROR] Docker not found
    echo Please install Docker: https://docs.docker.com/get-docker/
    exit /b 1
)
echo.

REM Check Docker Compose
echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker Compose is installed
    docker-compose --version
) else (
    echo [ERROR] Docker Compose not found
    echo Please install Docker Compose
    exit /b 1
)
echo.

REM Check Docker daemon
echo Checking Docker daemon...
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker daemon is running
) else (
    echo [ERROR] Docker daemon is not running
    echo Please start Docker Desktop
    exit /b 1
)
echo.

REM Check .env file
echo Checking .env file...
if exist .env (
    echo [OK] .env file found
    
    findstr /C:"OPENAI_API_KEY=your-openai-api-key" .env >nul
    if %errorlevel% equ 0 (
        echo [WARNING] OPENAI_API_KEY not set
    ) else (
        echo [OK] OPENAI_API_KEY is set
    )
    
    findstr /C:"GEMINI_API_KEY=your-gemini-api-key" .env >nul
    if %errorlevel% equ 0 (
        echo [WARNING] GEMINI_API_KEY not set
    ) else (
        echo [OK] GEMINI_API_KEY is set
    )
) else (
    echo [ERROR] .env file not found
    echo Run: copy .env.example .env
    exit /b 1
)
echo.

REM Check running services
echo Checking running services:
docker-compose ps
echo.

REM Check ports
echo Checking port availability:
netstat -an | findstr ":8080 " >nul && echo [OK] Port 8080 (API Gateway) - In use || echo [INFO] Port 8080 - Available
netstat -an | findstr ":8001 " >nul && echo [OK] Port 8001 (Ingestion) - In use || echo [INFO] Port 8001 - Available
netstat -an | findstr ":8002 " >nul && echo [OK] Port 8002 (Embedding) - In use || echo [INFO] Port 8002 - Available
netstat -an | findstr ":8003 " >nul && echo [OK] Port 8003 (Agent Router) - In use || echo [INFO] Port 8003 - Available
netstat -an | findstr ":6379 " >nul && echo [OK] Port 6379 (Redis) - In use || echo [INFO] Port 6379 - Available
netstat -an | findstr ":9000 " >nul && echo [OK] Port 9000 (MinIO) - In use || echo [INFO] Port 9000 - Available
echo.

echo ==========================================
echo Verification Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. If services are not running: start-all-docker.bat
echo 2. Access frontend: http://localhost:8080
echo 3. View logs: docker-compose logs -f
echo 4. Check status: docker-compose ps
echo.
