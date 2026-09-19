# System Health Monitoring & Logging

System health monitoring architecture and audit logging implementation.

## Real-Time Health Status Matrix

The backend `GET /health` endpoint continuously assesses operational state:

| Component | Assessment Criteria | Normal State | Failure State |
| :--- | :--- | :--- | :--- |
| **API** | FastAPI router operational | `healthy` | N/A |
| **FAISS** | Index loaded and chunks count $> 0$ | `ready` | `no_index` |
| **Embeddings** | MiniLM model instantiated | `ready` | `unavailable` |
| **Ollama** | Connection check to `http://localhost:11434/api/tags` | `connected` | `disconnected` |
| **LLM** | Target Ollama model name | `qwen2.5:1.5b` | N/A |

## Audit Event Logging

Application logs are managed via `setup_logger` in `src/utils/logging_config.py`.

Key logged events:
- Ingestion pipeline initialization & chunk indexing count
- Document deletion and FAISS index rebuilding
- RAG search results and similarity score breakdowns
- Ollama API connection exceptions and fallback triggers
- Technician feedback submission
