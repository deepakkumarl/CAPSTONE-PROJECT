# User Guide Overview

The Streamlit web interface (`app.py`) provides a clean, responsive diagnostic portal designed for BMW service technicians.

## Navigation Tabs

The portal is organized into four main operational tabs:

1. **💬 Diagnostic Assistant**: Conversational chat interface for submitting service questions, choosing preset diagnostic prompts, viewing grounded answers with source citations, and giving thumbs up/down feedback.
2. **📚 Knowledge Base Dashboard**: Real-time table listing all currently indexed documents, file formats, page counts, chunk counts, and document deletion controls.
3. **📜 Query History**: Historical log recording diagnostic queries, timestamps, response status (`success`/`fallback`), and retrieved documents.
4. **🧪 RAG Evaluation Benchmark**: Test runner tab that executes the automated benchmark suite item-by-item against the active RAG system with live progress indicators.

## Sidebar System Monitor

The left sidebar provides instant visibility into platform operational state:
- **API Status**: FastAPI connection indicator (`🟢`/`🔴`).
- **FAISS Status**: Index readiness state (`ready`/`no_index`).
- **Embeddings Status**: MiniLM model state (`ready`/`unavailable`).
- **Ollama Status**: Connection state to local Ollama server (`connected`/`disconnected`).
- **LLM**: Active Ollama model (`qwen2.5:1.5b`).
- **Knowledge Base Metrics**: Total documents count and total vector chunks count.
