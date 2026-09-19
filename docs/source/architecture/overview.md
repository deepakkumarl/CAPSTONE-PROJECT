# System Architecture Overview

The BMW Service Knowledge RAG platform is designed as a decoupled, modular 3-tier system operating 100% locally with zero cloud dependencies.

![Architecture Diagram](../_static/architecture.png)

## Component Breakdown

### 1. Presentation Tier (Streamlit UI)
- Interactive web portal (`app.py`) built using Streamlit.
- Provides multi-tab navigation:
  1. **Diagnostic Assistant**: Conversational chat interface with preset diagnostic queries and thumbs up/down user feedback widgets.
  2. **Knowledge Base Dashboard**: Document management table with file upload and single-click document deletion controls.
  3. **Query History**: Historical audit log of technician diagnostic queries.
  4. **RAG Evaluation Benchmark**: Real-time progress bar and item-by-item benchmark runner.
- Features sidebar system monitoring displaying active statuses (`🟢`/`🔴`) for API, FAISS, Embeddings, Ollama, and LLM.

### 2. Application Tier (FastAPI Backend)
- High-performance web service (`src/api/main.py` & `src/api/routes.py`) powered by FastAPI and Uvicorn.
- Exposes RESTful endpoints for document upload, knowledge base ingestion, RAG query execution, metadata listing, document deletion, and system health checks.
- Enforces request body validation using Pydantic models (`src/api/models.py`).

### 3. Intelligence & Storage Tier
- **Vector Store**: FAISS (`src/ai/vector_store.py`) storing 384-dimensional dense vectors with metadata docstore persistence.
- **Embeddings Model**: `sentence-transformers/all-MiniLM-L6-v2` (`src/ai/embeddings.py`) running locally on CPU.
- **LLM Server**: Ollama daemon (`src/ai/llm.py`) serving `qwen2.5:1.5b` locally at `http://localhost:11434`.
