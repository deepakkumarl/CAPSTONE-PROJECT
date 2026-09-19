# Health Monitoring & Logging Architecture

This document describes component health monitoring, audit logging, and system status indicators across the platform.

---

## 1. Health Monitoring Architecture

The system features real-time dependency checks available via `GET /health` and rendered visually on the Streamlit sidebar dashboard.

### Monitored Dependencies
1. **API**: FastAPI application router operational state (`healthy`).
2. **FAISS**: Vector index loading state and chunk availability (`ready` / `no_index`).
3. **Embeddings**: SentenceTransformers model state (`ready` / `unavailable`).
4. **Ollama**: External Ollama server connection check to `${OLLAMA_BASE_URL}/api/tags` (`connected` / `disconnected`).
5. **LLM**: Target model configuration (`qwen2.5:1.5b`).

### Overall System Status Criteria
- **`healthy`**: Ollama is connected AND FAISS index has ingested chunks.
- **`degraded`**: One or more non-critical or critical components are disconnected or uninitialized.

---

## 2. Structured Application Logging

Logging configuration is managed in `src/utils/logging_config.py`.

### Logged Events
- Document uploaded (filename, file size, target path)
- Document ingestion start & completion (document count, chunk count)
- Document deletion (chunks removed, FAISS index rebuilt)
- Query received & similarity search results (top chunks, score breakdown)
- Grounding level assignment (`HIGH`, `MEDIUM`, `INSUFFICIENT`)
- Ollama LLM requests & failure exceptions
- Technician feedback submission

### Secrets & Privacy Protection
Logs **NEVER** contain passwords, API keys, or raw full user credentials.
