# Developer Configuration Guide

Guidelines for configuring local development environments.

## Development Environment Setup

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install development and documentation dependencies
pip install -r requirements.txt
pip install -r docs/requirements-docs.txt
```

## Environment File Overrides

Developers can override default settings by creating a `.env` file in the root directory:

```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=5
SIMILARITY_THRESHOLD=0.35
CHUNK_SIZE=800
CHUNK_OVERLAP=100
```
