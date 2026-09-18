# BMW Service Knowledge RAG

An enterprise-grade, end-to-end Retrieval-Augmented Generation (RAG) capstone project designed for BMW service technicians. Technicians can ask complex vehicle diagnostic questions and receive grounded, accurate answers backed strictly by cited BMW service documentation using a local Ollama LLM (`qwen2.5:1.5b`).

![Architecture Diagram](docs/architecture.png)

---

## Overview

The **BMW Service Knowledge RAG** system bridges technical service documentation and master mechanics. It automates text extraction, clean chunking, dense vector indexing, threshold-validated similarity retrieval, and strict grounded answer generation. All processing runs 100% locally on standard developer hardware with zero external API costs or data privacy egress.

---

## Problem Statement

BMW service technicians face tight repair timelines and must quickly consult complex service manuals, technical bulletins, and fault code matrices. Generic LLMs tend to introduce hallucinations, invent torque specifications, or suggest invalid procedures. This system enforces strict pre-retrieval validation:
- **Retrieves relevant service documentation BEFORE generating any answer.**
- **Enforces zero outside knowledge usage.**
- **If documentation is insufficient, explicitly states:**
  > *"I could not find sufficient information in the available BMW service documentation."*

---

## Architecture

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
         FAISS Vector Store
                  │
                  ▼
         Retriever (Threshold 0.35)
                  │
                  ▼
       LangChain RAG Pipeline ──► Ollama (qwen2.5:1.5b)
                  │
                  ▼
       FastAPI Backend Server
                  │
                  ▼
       Streamlit Frontend UI
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
- **Testing**: PyTest, FastAPI TestClient (`httpx`)
- **DevOps / Infra**: Docker, GitHub Actions, Terraform (placeholder)

---

## Project Structure

```
bmw-capstone-usecase/
├── README.md                          # Comprehensive Project Guide
├── app.py                             # Streamlit Frontend UI
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
│   └── vectorstore/                   # Persistent FAISS Index Files (gitignored)
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── document_loader.py        # PDF, TXT, DOCX, CSV Loaders
│   │   └── ingest.py                 # Pipeline Ingestion Coordinator
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── text_cleaner.py           # Whitespace & Line Normalizer
│   │   └── chunker.py                # Recursive Text Chunker with Metadata
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── embeddings.py             # Local HuggingFace Embeddings
│   │   ├── vector_store.py           # FAISS Storage & Similarity Search
│   │   ├── retriever.py              # Relevant Chunk Retriever & Filter
│   │   ├── llm.py                    # Ollama LLM Connection
│   │   └── rag.py                    # Grounded RAG Pipeline Orchestrator
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI Application Entrypoint
│   │   ├── models.py                 # Pydantic Schemas
│   │   └── routes.py                 # REST API Endpoints (/health, /ingest, /query, /documents)
│   └── utils/
│       ├── __init__.py
│       ├── config.py                 # Application Settings
│       └── logging_config.py         # Standard Logger Setup
├── sql/
│   └── README.md                      # Relational Metadata Storage Notes
├── terraform/
│   └── main.tf                        # Local Infrastructure Manifest
├── .github/
│   └── workflows/
│       └── tests.yml                  # GitHub Actions CI Workflow
└── tests/
    ├── __init__.py
    ├── test_text_cleaner.py
    ├── test_chunker.py
    ├── test_metadata.py
    ├── test_api_health.py
    ├── test_query_validation.py
    ├── test_empty_query.py
    ├── test_rag_prompt.py
    └── test_retrieval_formatting.py
```

---

## Prerequisites

Before starting, ensure the following software is installed on your local laptop:
1. **Python 3.10+**: `python --version`
2. **Ollama**: Download and install from [ollama.ai](https://ollama.ai)
3. **Ollama Model**: `qwen2.5:1.5b`

---

## Installation

### 1. Clone Repository & Create Virtual Environment
```bash
git clone <repository_url>
cd bmw-capstone-usecase

# Create virtual environment
python -m venv .venv
```

**Activate virtual environment:**
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install & Verify Local LLM (Ollama)
```bash
# Pull lightweight qwen2.5:1.5b model
ollama pull qwen2.5:1.5b

# Verify Ollama serve status
ollama list
```

---

## Environment Variables

Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env
```

Default values in `.env.example`:
```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=4
CHUNK_SIZE=800
CHUNK_OVERLAP=100
SIMILARITY_THRESHOLD=0.35
BACKEND_URL=http://localhost:8000
```

---

## Running the Backend

Start the FastAPI application server using Uvicorn:
```bash
uvicorn src.api.main:app --reload
```
- **Backend API**: `http://localhost:8000`
- **Swagger Interactive API Docs**: `http://localhost:8000/docs`

---

## Running Streamlit Frontend

In a new terminal window (with `.venv` active):
```bash
streamlit run app.py
```
- **Streamlit Web Application**: `http://localhost:8501`

---

## Ingesting Documents

You can trigger ingestion in two ways:
1. **Via Streamlit UI**: Click **"Ingest Sample Documents"** in the sidebar, or use the file uploader to index custom PDFs/TXT files.
2. **Via API**: Send a `POST` request to `http://localhost:8000/ingest` or upload via `POST /upload`.

---

## Benchmark Example Query & Response

### Technician Question:
> *"What should be checked when an EV reports repeated battery overheating?"*

### Expected Grounded Answer:
> When an electric vehicle reports repeated high-voltage (HV) battery overheating or fault codes 21A004 / 21A008, check the following:
> 1. **Coolant Circuit & Level**: Inspect fluid level in the secondary expansion reservoir, check coolant pump V54 for speed feedback and cavitation, and perform a 1.5 bar pressure leak test.
> 2. **Fault Code Readout**: Connect ISTA/D interface to read TMCU and CMC DTCs (21A004 and 21A008).
> 3. **Temperature Sensor Inspection**: Monitor live values across all 12 internal module NTC sensors. If any module strays >8°C from average, inspect thermal pads.
> 4. **Heat Exchanger & Valves**: Inspect chiller shut-off valve Y102 and refrigerant expansion valve Y104.

### Cited Sources:
- `sample_ev_battery_service.txt` — Page 1 (Score: 0.88)

---

## Running Unit & Integration Tests

Run the full pytest suite (all LLM external calls are mocked):
```bash
pytest --verbose
```

---

## Docker Support

Build and launch the FastAPI backend in Docker:
```bash
# Build Docker image
docker build -t bmw-rag-backend .

# Run container connecting to host Ollama
docker run -p 8000:8000 --add-host=host.docker.internal:host-gateway bmw-rag-backend
```

---

## Limitations

- **Synthetic Sample Data**: Included documentation (`data/sample/`) consists of non-copyrighted synthetic procedures created for demonstration purposes.
- **Lightweight Local LLM**: `qwen2.5:1.5b` is optimized for local developer laptop execution. Complex multi-page reasoning may benefit from larger models (`qwen2.5:7b`).
- **Demonstration Software**: This project is an educational capstone and not an official replacement for official BMW ISTA diagnostic hardware or service software.

---

## Future Enhancements

1. **Re-ranking**: Integrate Cohere or CrossEncoder re-rankers for enhanced precision.
2. **Hybrid Search**: Combine BM25 keyword search with dense FAISS vectors.
3. **OCR Integration**: Add Tesseract / Unstructured OCR for scanned legacy PDF wiring diagrams.
4. **Multilingual Support**: Enable German / English technical term translation.
5. **Document Versioning & Audit Logs**: Add SQL persistence for technician query logs and manual feedback.
