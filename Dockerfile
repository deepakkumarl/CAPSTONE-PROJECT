FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for optimal layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create directory for vectorstore and uploads
RUN mkdir -p data/vectorstore data/uploads data/sample

# Expose FastAPI backend port
EXPOSE 8000

# Set environment defaults (Ollama running on host)
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434
ENV OLLAMA_MODEL=qwen2.5:1.5b
ENV BACKEND_URL=http://0.0.0.0:8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
