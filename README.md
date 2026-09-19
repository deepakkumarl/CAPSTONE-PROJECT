# BMW Service Knowledge RAG Capstone

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![FAISS](https://img.shields.io/badge/FAISS-CPU-orange.svg)](https://github.com/facebookresearch/faiss)
[![Ollama](https://img.shields.io/badge/Ollama-qwen2.5:1.5b-purple.svg)](https://ollama.ai/)

Production-ready local Retrieval-Augmented Generation (RAG) assistant for BMW service technicians. Delivers grounded diagnostic procedures, multi-format document indexing, deduplicated citations, automated evaluation benchmarks, and full component health monitoring.

---

## 1. Project Overview
The **BMW Service Knowledge RAG** platform provides automotive service technicians with instant, grounded access to technical manuals, diagnostic flowcharts, EV battery service procedures, and thermal management specifications. Operating 100% locally with zero cloud dependencies, it ensures complete data privacy and high diagnostic reliability.

---

## 📚 Professional Sphinx Documentation Site
The project includes an enterprise-grade Sphinx documentation website powered by the **Furo** theme and **MyST Parser**.

### Building & Viewing Documentation Locally
```bash
# Install documentation dependencies
pip install -r docs/requirements-docs.txt

# Build HTML documentation using Sphinx
sphinx-build -b html docs/source docs/build/html
```

After building, open `docs/build/html/index.html` in your web browser.

### Documentation Navigation Overview
- **Home**: Project overview, key capabilities, architecture diagram, badges, and quick start.
- **Getting Started**: Installation, environment configuration, and server execution.
- **Architecture**: System components, RAG pipeline execution, data flows, and FAISS vector store.
- **User Guide**: Streamlit multi-tab portal instructions, document upload, querying, and deletion.
- **API Reference**: REST API specifications for `/health`, `/upload`, `/ingest`, `/query`, `/documents`, `/feedback`.
- **RAG & AI**: Document processing, chunking, embeddings, retrieval algorithms, grounding, and LLM prompt templates.
- **Data & Storage**: Data dictionary, metadata schemas, FAISS spec, and JSON persistence.
- **Testing & Evaluation**: Pytest strategy, test coverage reporting, and evaluation benchmark.
- **Security**: Path traversal prevention, file upload controls, and Bandit AST security analysis.
- **CI/CD**: GitHub Actions pipeline, Flake8, SonarCloud, Docker, and Docker Hub deployment.
- **Monitoring**: Real-time health check matrix and structured audit logging.
- **Developer Guide**: Codebase structure, local development environment, and contribution guide.

---

## 2. Business Problem
Modern BMW vehicles (electric, hybrid, internal combustion) feature intricate technical manuals spanning thousands of pages. Technicians often spend up to 20% of diagnostic time locating accurate wiring diagrams, sensor voltage limits, or torque specifications. Generic cloud AI assistants risk hallucinating safety-critical repair steps. This platform eliminates search overhead while guaranteeing strictly grounded answers derived exclusively from verified BMW documentation.

---

## 3. Architecture

```
                                  +-----------------------+
                                  | Streamlit Frontend    |
                                  | (Port 8501)           |
                                  +-----------+-----------+
                                              |
                                              v  HTTP / REST API
                                  +-----------+-----------+
                                  |  FastAPI Backend      |
                                  |  (Port 8000)          |
                                  +-----+-----------+-----+
                                        |           |
               +------------------------+           +-----------------------+
               |                                                            |
               v                                                            v
+--------------+--------------+                              +--------------+--------------+
| FAISS Vector Store          |                              | Ollama LLM Server           |
| (sentence-transformers/     |                              | (qwen2.5:1.5b)              |
|  all-MiniLM-L6-v2)          |                              | (Port 11434)                |
+-----------------------------+                              +-----------------------------+
```

---

## 4. Technology Stack
- **Frontend**: Streamlit 1.25+
- **Backend API**: FastAPI 0.100+, Uvicorn
- **Vector Database**: FAISS (CPU)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Local LLM**: Ollama (`qwen2.5:1.5b`)
- **Document Parsers**: `pypdf`, `python-docx`, Python CSV, standard text
- **Testing & Coverage**: Pytest, Pytest-Cov, FastAPI TestClient
- **Quality & Security**: Flake8, Bandit, SonarQube / SonarCloud
- **Containerization**: Docker, Docker Compose

---

## 5. Project Structure
```
bmw-capstone-usecase/
├── .github/
│   └── workflows/
│       └── tests.yml            # CI/CD GitHub Actions pipeline
├── data/
│   ├── sample/                  # Sample BMW service documentation
│   ├── uploads/                 # Uploaded technician documents
│   ├── vectorstore/             # FAISS index files (index.faiss, index.pkl)
│   ├── query_history.json       # Query execution history
│   └── feedback.json            # Technician user feedback log
├── docs/                        # Complete capstone documentation
│   ├── PRD.md                   # Product Requirement Document
│   ├── API.md                   # API Specifications
│   ├── data_dictionary.md       # Data Schemas & Dictionary
│   ├── testing.md               # Testing Strategy
│   ├── deployment.md            # Local & Container Setup
│   ├── security.md              # Security Controls & Scanning
│   ├── monitoring.md            # Health & Audit Logging
│   └── UAT.md                   # User Acceptance Testing Protocol
├── src/
│   ├── ai/                      # Vector store, embeddings, retriever, LLM, RAG, evaluation
│   ├── api/                     # FastAPI main app, routers, Pydantic models
│   ├── ingestion/               # Document loaders and ingestion pipeline
│   ├── processing/              # Text cleaner and chunker
│   └── utils/                   # Configuration, history, feedback, logging
├── tests/                       # Automated Pytest suite
├── app.py                       # Streamlit multi-tab user interface
├── Dockerfile                   # Docker build container definition
├── docker-compose.yml           # Multi-container orchestration
├── sonar-project.properties     # SonarQube configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Main project README
```

---

## 6. Prerequisites
- Python 3.11+
- Git
- Docker Desktop (optional for containerized execution)
- Ollama installed locally

---

## 7. Ollama Setup
1. Download & install Ollama from [ollama.ai](https://ollama.ai).
2. Start the local Ollama service. Default endpoint: `http://localhost:11434`.

---

## 8. qwen2.5:1.5b Setup
Pull the required LLM model:
```bash
ollama pull qwen2.5:1.5b
```

---

## 9. Python Environment Setup
```bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\Activate.ps1
# Activate on Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 10. Backend Startup
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation: `http://localhost:8000/docs`

---

## 11. Streamlit Startup
In a separate terminal tab:
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`.

---

## 12. Document Ingestion
Trigger ingestion via UI ("Re-index Sample Knowledge Base Directory" or "Upload Documentation") or via API:
```bash
curl -X POST http://localhost:8000/ingest
```

---

## 13. Query Examples
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What should be checked when an EV reports repeated battery overheating?",
    "top_k": 5,
    "similarity_threshold": 0.35
  }'
```

---

## 14. API Endpoints
- `GET /health`: System component status
- `POST /ingest`: Bulk ingestion
- `POST /upload`: Single document upload & index
- `POST /query`: Grounded technical query
- `GET /documents`: List indexed files
- `DELETE /documents/{filename}`: Safe document deletion & index rebuild
- `GET /history`: Technician query history log
- `POST /feedback`: Submit user feedback
- `GET /evaluate`: Run RAG evaluation suite

---

## 15. Testing
Run the automated Pytest suite:
```bash
pytest --verbose
```

---

## 16. Coverage
Generate terminal and XML coverage reports:
```bash
pytest --cov=src --cov-report=term-missing --cov-report=xml
```

---

## 17. CI/CD
GitHub Actions workflow configured in `.github/workflows/tests.yml`:
- Triggered on push / pull request to `main`
- Runs flake8 linting, bandit security scan, pytest coverage, SonarQube analysis, and Docker image build.

---

## 18. SonarQube / SonarCloud
Configured via `sonar-project.properties`. Uploads code quality metrics, code smell detections, and `coverage.xml` test coverage data.

---

## 19. Security Scanning
Lightweight AST security scanning using **Bandit**:
```bash
bandit -r src
```
File upload path traversal prevention and 10MB size limit controls enforced in `src/api/routes.py`.

---

## 20. Docker
Build image and run multi-container stack:
```bash
docker-compose up --build -d
```

---

## 21. Failure and Recovery Behavior
- **Ollama Offline**: API returns clean error message (`"Error communicating with local LLM (Ollama)..."`). Backend API does not crash. Component status in `/health` updates to `disconnected` 🔴.
- **Corrupt FAISS**: Handled safely returning empty document list until re-indexed.

---

## 22. RAG Evaluation
Automated benchmark evaluating retrieval precision, grounded response generation, and anti-hallucination fallback on out-of-domain queries. Access via `GET /evaluate` or UI tab *"RAG Evaluation Benchmark"*.

---

## 23. Known Limitations
- Local CPU inference speed depends on host CPU/RAM specifications.
- OCR for image-only PDFs is not included out-of-the-box (requires Tesseract).

---

## 24. Future Enhancements
- Support for multimodal diagnostic diagrams (image/schematic input).
- PostgreSQL / PGVector optional backend storage for enterprise scale.
- Multi-language technical translation for global technician support.
