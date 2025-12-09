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
COPY services/stock_producer/ ./services/stock_producer/

# Create directories
RUN mkdir -p /app/data /app/logs

ENV PYTHONPATH=/app

EXPOSE 8005

CMD ["python", "-m", "services.stock_producer.main"]
