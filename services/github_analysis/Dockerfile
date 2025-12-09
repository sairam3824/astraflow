FROM python:3.11-slim

# Install system dependencies including git for GitHub operations
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared libraries
COPY libs/ ./libs/

# Copy service code
COPY services/github_analysis/ ./services/github_analysis/

# Create directories
RUN mkdir -p /app/data /app/logs

ENV PYTHONPATH=/app

EXPOSE 8007

CMD ["python", "-m", "services.github_analysis.main"]
