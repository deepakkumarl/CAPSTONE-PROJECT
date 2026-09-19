# Testing Strategy & Guidelines

This document outlines the testing architecture, pytest suite structure, mocking practices, and coverage standards for the BMW Service Knowledge RAG Capstone.

---

## 1. Unit & Integration Test Architecture

All automated tests are built using **Pytest** and **FastAPI TestClient**.

### Deterministic Test Execution
- Tests **MUST NOT** require a running local Ollama server during CI/CD execution.
- External LLM invocations (`get_llm`, `ChatOllama.invoke`) and external network requests (`requests.get`) are fully mocked using `unittest.mock.patch`.
- Local sentence transformers (`sentence-transformers/all-MiniLM-L6-v2`) or mock embedding instances are used during testing.

---

## 2. Running Tests Locally

### Run Complete Test Suite
```bash
pytest --verbose
```

### Run Test Suite with Coverage
```bash
pytest --cov=src --cov-report=term-missing --cov-report=xml
```

---

## 3. Key Test Categories

| Test File | Target Area | Description |
|---|---|---|
| `test_api_health.py` | API / Health | Validates `/health` endpoint structure |
| `test_enhanced_health.py` | API / Components | Validates component-level health checks |
| `test_chunker.py` | Processing | Validates text splitting, chunk sizing, and metadata assignment |
| `test_document_deletion.py` | Vector Store / API | Tests document deletion, index rebuilding, 404 handling |
| `test_empty_query.py` | API / Validation | Verifies 400 Bad Request on blank queries |
| `test_evaluation.py` | Evaluation | Tests single test case evaluation and benchmark suite runners |
| `test_feedback.py` | API / Feedback | Tests `/feedback` endpoint and JSON persistence |
| `test_ingestion_formats.py` | Ingestion | Tests loading PDF, TXT, DOCX, CSV formats |
| `test_resilience_and_errors.py` | Resilience | Tests Ollama offline, corrupt FAISS, path traversal, empty upload |
| `test_source_deduplication.py` | Retriever | Verifies source deduplication by `(document, page)` and `chunk_id` |

---

## 4. Test Coverage Thresholds

- **Target Coverage**: $\ge 80\%$ on application source code (`src/`).
- Coverage reports are generated in `coverage.xml` for SonarQube / GitHub Actions integration.
