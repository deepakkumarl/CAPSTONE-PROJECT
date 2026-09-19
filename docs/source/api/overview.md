# REST API Overview

The BMW Service Knowledge RAG platform exposes high-performance RESTful endpoints built using FastAPI and Uvicorn.

## Base URL
- **Local Development**: `http://localhost:8000`
- **Docker Container**: `http://backend:8000`

## Interactive OpenAPI Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc UI**: `http://localhost:8000/redoc`

## Endpoints Summary

| Method | Endpoint | Description | Request Model | Response Model |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Enhanced health & component monitoring | None | `HealthResponse` |
| `POST` | `/ingest` | Trigger bulk knowledge base ingestion | None | `IngestResponse` |
| `POST` | `/upload` | Upload & ingest multi-format document | `UploadFile` | `IngestResponse` |
| `POST` | `/query` | Query RAG pipeline for grounded answer | `QueryRequest` | `QueryResponse` |
| `GET` | `/documents` | List indexed documents and statistics | None | `DocumentListResponse` |
| `DELETE` | `/documents/{filename}` | Delete document and rebuild FAISS index | None | `DeleteDocumentResponse` |
| `GET` | `/history` | Retrieve local query execution log | Query params | `QueryHistoryResponse` |
| `POST` | `/feedback` | Submit technician user feedback | `FeedbackRequest` | `FeedbackResponse` |
| `GET` | `/evaluate/dataset` | Fetch benchmark dataset test cases | None | `BenchmarkDatasetResponse` |
| `POST` | `/evaluate/test-case` | Evaluate single benchmark test case | `TestCaseRequest` | `TestCaseResult` |
| `GET` | `/evaluate` | Run full benchmark test suite | None | `EvaluationReport` |
