import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/astraflow.db")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # MinIO
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "documents")
    
    # ChromaDB
    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    
    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Services
    API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT", "8000"))
    INGESTION_SERVICE_PORT = int(os.getenv("INGESTION_SERVICE_PORT", "8001"))
    EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT", "8002"))
    AGENT_ROUTER_PORT = int(os.getenv("AGENT_ROUTER_PORT", "8003"))
    WORKFLOW_RUNNER_PORT = int(os.getenv("WORKFLOW_RUNNER_PORT", "8004"))
    STOCK_PRODUCER_PORT = int(os.getenv("STOCK_PRODUCER_PORT", "8005"))
    STOCK_ANALYSIS_PORT = int(os.getenv("STOCK_ANALYSIS_PORT", "8006"))
    GITHUB_ANALYSIS_PORT = int(os.getenv("GITHUB_ANALYSIS_PORT", "8087"))

config = Config()
