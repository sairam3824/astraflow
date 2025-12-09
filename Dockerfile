# Multi-stage build for Python services
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY libs/ ./libs/
COPY services/ ./services/
COPY templates/ ./templates/

# Create data and logs directories
RUN mkdir -p /app/data /app/logs

# Set Python path
ENV PYTHONPATH=/app

# Default command (will be overridden in docker-compose)
CMD ["python", "-m", "services.api_gateway.main"]
