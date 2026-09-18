# BMW Service Knowledge RAG

An enterprise-grade, end-to-end Retrieval-Augmented Generation (RAG) capstone project designed for BMW service technicians. Technicians can ask complex vehicle diagnostic questions and receive grounded, accurate answers backed strictly by cited BMW service documentation using a local Ollama LLM (`qwen2.5:1.5b`).

![Architecture Diagram](docs/architecture.png)

---

## Overview

The **BMW Service Knowledge RAG** platform bridges technical service documentation and master mechanics. It features:
- **Multi-Tab Streamlit Technician Interface**: Diagnostic Assistant, Knowledge Base Dashboard, Query History, and RAG Evaluation Benchmark.
- **Strict Grounding & Anti-Hallucination**: Answers are derived ONLY from retrieved context. If information is missing, the assistant outputs:
  > *"I could not find sufficient information in the available BMW service documentation."*
- **Source Deduplication**: Duplicate source citations from identical document pages are automatically deduplicated.
- **Document Management**: Supports PDF, TXT, DOCX, and CSV formats with duplicate ingestion prevention and document deletion with vector store index rebuilding.
- **Local Query History & Evaluation Suite**: Records recent queries and provides automated RAG benchmark evaluation reports.
- **100% Privacy & Local Execution**: All embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and LLM generation (`qwen2.5:1.5b` via Ollama) run locally with zero API costs.

---

## Architecture Flow

### Ingestion Pipeline Flow:
```
BMW Service Documents (PDF, TXT, DOCX, CSV)
                  │
                  ▼
         Document Loader
                  │
                  ▼
         Text Processing & Cleaner
                  │
                  ▼
   Recursive Chunker (800 / 100 overlap)
                  │
                  ▼
Local SentenceTransformers (all-MiniLM-L6-v2)
                  │
                  ▼
    FAISS Vector Store Persistence
```

### Retrieval & Diagnostic Query Flow:
```
Technician Question ──► Streamlit UI ──► FastAPI Backend
                                             │
                                             ▼
                                  FAISS Top-K Search
                                             │
                                             ▼
                                Relevant Source Deduplication
                                             │
                                             ▼
                                  Relevance Threshold Check
                                  │                       │
                               (Pass)                   (Fail)
                                  │                       │
                                  ▼                       ▼
                     Strict Grounding Prompt       Fallback Answer
                                  │
                                  ▼
                         Ollama (qwen2.5:1.5b)
                                  │
                                  ▼
                         Grounded Answer + Sources ──► Streamlit UI
```

---

## Technology Stack

- **Frontend**: Streamlit (Python)
- **Backend API**: FastAPI, Uvicorn
- **RAG Framework**: LangChain (`langchain-community`, `langchain-ollama`, `langchain-huggingface`)
- **Vector Database**: FAISS (`faiss-cpu`)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (Local HuggingFace)
- **Local LLM**: Ollama with `qwen2.5:1.5b`
- **Document Processing**: PyPDF (`pypdf`), `python-docx`, plain text, CSV
- **Query History & Evaluation**: Local JSON history (`data/query_history.json`), Automated benchmark test suite (`src/ai/evaluation.py`)
- **Testing**: PyTest, FastAPI TestClient (`httpx`)
- **DevOps / Infra**: Docker, GitHub Actions, Terraform (placeholder)

---

## Project Structure

```
bmw-capstone-usecase/
├── README.md                          # Comprehensive Project Guide
├── app.py                             # Streamlit Multi-Tab Frontend UI
├── requirements.txt                   # Dependency Specification
├── Dockerfile                         # Backend Container Build Specification
├── .env.example                       # Environment Configuration Template
├── .gitignore                         # Repository Ignore File
├── docs/
│   ├── PRD.md                         # Product Requirement Document
│   ├── architecture.png               # System Architecture Visual Diagram
│   ├── data_dictionary.md             # Schema & Field Metadata Documentation
│   └── generate_diagram.py            # Diagram Generator Script
├── data/
│   ├── sample/                        # Synthetic BMW Technical Documents
│   │   ├── sample_ev_battery_service.txt
│   │   ├── sample_thermal_management.txt
│   │   └── sample_charging_system.txt
│   ├── uploads/                       # User Uploaded Documents
│   ├── query_history.json             # Local Diagnostic Query History Log
│   └── vectorstore/                   # Persistent FAISS Index Files (gitignored)
├── src/
│   ├── ingestion/
│   │   ├── document_loader.py        # PDF, TXT, DOCX, CSV Loaders
│   │   └── ingest.py                 # Ingestion Pipeline Coordinator
│   ├── processing/
│   │   ├── text_cleaner.py           # Whitespace & Line Normalizer
│   │   └── chunker.py                # Recursive Text Chunker with Metadata
│   ├── ai/
│   │   ├── embeddings.py             # Local HuggingFace Embeddings
│   │   ├── vector_store.py           # FAISS Storage, Deduplication & Deletion
│   │   ├── retriever.py              # Deduplicated Chunk Retriever & Filter
│   │   ├── llm.py                    # Ollama LLM Connection
│   │   ├── rag.py                    # Grounded RAG Pipeline Orchestrator
│   │   └── evaluation.py             # Automated RAG Benchmark Suite
│   ├── api/
│   │   ├── main.py                   # FastAPI Application Entrypoint
│   │   ├── models.py                 # Pydantic Schemas
│   │   └── routes.py                 # REST API Endpoints (/health, /ingest, /query, /documents, /history, /evaluate)
│   └── utils/
│       ├── config.py                 # Application Settings
│       ├── logging_config.py         # Standard Logger Setup
│       └── history.py                # Local Query History Manager
├── sql/
│   └── README.md                      # Relational Metadata Storage Notes
├── terraform/
│   └── main.tf                        # Local Infrastructure Manifest
├── .github/
│   └── workflows/
│       └── tests.yml                  # GitHub Actions CI Workflow
└── tests/                             # PyTest Test Suite
    ├── test_text_cleaner.py
    ├── test_chunker.py
    ├── test_metadata.py
    ├── test_api_health.py
    ├── test_query_validation.py
    ├── test_empty_query.py
    ├── test_rag_prompt.py
    ├── test_retrieval_formatting.py
    ├── test_source_deduplication.py
    ├── test_document_deletion.py
    ├── test_query_history.py
    ├── test_evaluation.py
    ├── test_enhanced_health.py
    └── test_ingestion_formats.py
```

---

## Installation & Setup

### 1. Environment & Dependencies
```bash
git clone <repository_url>
cd bmw-capstone-usecase

# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\activate

# Linux / macOS:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Ollama Local LLM Setup
```bash
# Install Ollama from https://ollama.ai
# Pull qwen2.5:1.5b model
ollama pull qwen2.5:1.5b

# Verify Ollama status
ollama serve
```

---

## Running the Application

### 1. Start FastAPI Backend
```bash
uvicorn src.api.main:app --reload
```
- API Base URL: `http://localhost:8000`
- Swagger UI Docs: `http://localhost:8000/docs`

### 2. Start Streamlit Frontend UI
```bash
streamlit run app.py
```
- Web App URL: `http://localhost:8501`

---

## REST API Endpoints

- `GET /health`: Structured status for API, FAISS, Embeddings, and Ollama connection.
- `POST /ingest`: Ingests sample service documents into vector index.
- `POST /upload`: Uploads and indexes PDF, TXT, DOCX, or CSV files.
- `POST /query`: Submits question with dynamic `top_k` and `similarity_threshold` parameters.
- `GET /documents`: Returns indexed documents table data.
- `DELETE /documents/{filename}`: Deletes document and rebuilds FAISS index.
- `GET /history`: Returns local technician query history logs.
- `GET /evaluate`: Executes automated RAG benchmark evaluation test suite.

---

## Benchmark Example Diagnostic Query

### Technician Question:
> *"What should be checked when an EV reports repeated battery overheating?"*

### Grounded Response:
> When an electric vehicle reports repeated high-voltage (HV) battery overheating or fault codes 21A004 / 21A008, check:
> 1. **Coolant Circuit & Level**: Fluid level in expansion reservoir, coolant pump V54 speed feedback, and 1.5 bar leak test.
> 2. **Fault Code Readout**: Connect ISTA/D to read TMCU and CMC DTCs (21A004 & 21A008).
> 3. **Temperature Sensors**: Live NTC sensor readings across 12 battery modules.
> 4. **Chiller & Valves**: Chiller shut-off valve Y102 and refrigerant expansion valve Y104.

### Deduplicated Sources:
- `sample_ev_battery_service.txt` — Page 1 (Relevance: 0.88)

---

## Testing

Run the comprehensive pytest suite (all LLM calls are mocked):
```bash
pytest --verbose
```

---

## Limitations & Disclaimer

- **Synthetic Sample Data**: Included files in `data/sample/` consist of non-copyrighted synthetic diagnostic procedures created for demonstration purposes.
- **Developer Hardware Optimization**: `qwen2.5:1.5b` is lightweight for laptop execution.
- **Capstone Project**: Educational project; not an official replacement for BMW ISTA hardware or official service documentation.
