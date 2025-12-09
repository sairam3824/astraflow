FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries
COPY libs/ ./libs/

# Copy service code
COPY services/agent_router/ ./services/agent_router/

# Create directories
RUN mkdir -p /app/data /app/logs

ENV PYTHONPATH=/app

EXPOSE 8003

CMD ["python", "-m", "services.agent_router.main"]
