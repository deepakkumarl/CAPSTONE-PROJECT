# Running the Application

This guide explains how to start and operate the FastAPI backend server, Streamlit frontend UI, and Docker containers.

## 1. Local Native Startup

### Step 1: Ensure Ollama is Running
Ensure the Ollama daemon is active and `qwen2.5:1.5b` is loaded:
```bash
ollama run qwen2.5:1.5b "Hello"
```

### Step 2: Launch FastAPI Backend Server
In the activated virtual environment:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Interactive Swagger Docs**: Open `http://localhost:8000/docs`
- **ReDoc API Docs**: Open `http://localhost:8000/redoc`

### Step 3: Launch Streamlit Frontend Interface
In a second terminal window:
```bash
streamlit run app.py
```
- **Technician Dashboard UI**: Open `http://localhost:8501`

---

## 2. Docker & Docker Compose Startup

### Option A: Docker Compose (Recommended)
Run the complete multi-container stack:
```bash
docker-compose up --build -d
```

- **FastAPI Container**: `http://localhost:8000`
- **Streamlit Container**: `http://localhost:8501`
- **Published Image**: `deepakkumar889/bmw-service-rag:latest`

### Option B: Direct Docker Container Execution
```bash
# Build the Docker image
docker build . -t bmw-service-rag:latest

# Run the container linking to host Ollama
docker run -d -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=qwen2.5:1.5b \
  --name bmw-rag-backend \
  bmw-service-rag:latest
```
