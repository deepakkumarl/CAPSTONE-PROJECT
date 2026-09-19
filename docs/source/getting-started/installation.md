# Installation Guide

This document outlines the step-by-step procedures for installing all required runtime dependencies for the BMW Service Knowledge RAG platform.

## 1. Prerequisites

Before installing the platform, ensure the following software tools are installed on your host system:

- **Python**: Version 3.11 or higher
- **Git**: For repository version control
- **Ollama**: Installed locally from [ollama.ai](https://ollama.ai)
- **Docker & Docker Compose**: Optional, for multi-container orchestration

## 2. Environment Setup

Clone the repository and set up an isolated Python virtual environment:

```bash
# Clone the repository
git clone https://github.com/deepakkumar889/bmw-capstone-usecase.git
cd bmw-capstone-usecase

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

## 3. Install Python Dependencies

Install the required Python packages specified in `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Required Core Packages
- `fastapi` & `uvicorn`: Web API framework and ASGI server
- `streamlit`: Multi-tab technician web interface
- `langchain`, `langchain-community`, `langchain-ollama`, `langchain-huggingface`: RAG orchestrators
- `faiss-cpu`: Local vector similarity search library
- `sentence-transformers`: Local text embedding generation (`all-MiniLM-L6-v2`)
- `pypdf`, `python-docx`: Multi-format document extraction libraries

## 4. Ollama LLM Model Installation

Pull the default local model `qwen2.5:1.5b` via the Ollama CLI:

```bash
ollama pull qwen2.5:1.5b
```

Verify that Ollama is responding on `http://localhost:11434`:

```bash
curl http://localhost:11434/api/tags
```
