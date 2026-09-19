# Deployment & Containerization Guide

This document explains how to set up, build, run, and containerize the BMW Service Knowledge RAG platform locally and with Docker / Docker Compose.

---

## 1. Local Development Execution

### Prerequisites
1. Python 3.11+
2. Ollama installed locally (`http://localhost:11434`)
3. Ollama model pulled:
   ```bash
   ollama pull qwen2.5:1.5b
   ```

### Setup Virtual Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Start Backend API
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend UI
```bash
streamlit run app.py
```

---

## 2. Docker & Docker Compose Execution

### Docker Image Build
```bash
docker build . -t bmw-service-rag:latest
```

### Docker Compose Multi-Container Orchestration
```bash
docker-compose up --build -d
```

- **Backend API**: `http://localhost:8000`
- **Streamlit UI**: `http://localhost:8501`
- Host Ollama communication is configured via `OLLAMA_BASE_URL=http://host.docker.internal:11434`.
