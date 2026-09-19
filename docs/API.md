# API Reference Documentation

The BMW Service Knowledge RAG platform exposes RESTful endpoints powered by FastAPI and Uvicorn.

## Base URL
Default: `http://localhost:8000`

---

## Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System component health check (API, FAISS, Embeddings, Ollama) |
| `POST` | `/ingest` | Ingest sample data directory into FAISS index |
| `POST` | `/upload` | Upload & ingest single PDF, TXT, DOCX, or CSV document |
| `POST` | `/query` | Submit diagnostic question to RAG pipeline |
| `GET` | `/documents` | List indexed documents and chunk statistics |
| `DELETE` | `/documents/{filename}` | Delete document and rebuild FAISS vector index |
| `GET` | `/history` | Retrieve local query execution history |
| `POST` | `/feedback` | Submit technician feedback (thumbs up/down) |
| `GET` | `/evaluate/dataset` | Fetch benchmark test suite definitions |
| `POST` | `/evaluate/test-case` | Evaluate single benchmark test case |
| `GET` | `/evaluate` | Run full automated benchmark test suite |

---

## Detailed Endpoint Specifications

### `GET /health`
Returns system status for backend API, vector index, embedding model, and Ollama connection.

**Response `200 OK`**:
```json
{
  "status": "healthy",
  "api": "healthy",
  "vector_store": "ready",
  "embeddings": "ready",
  "ollama": "connected",
  "llm": "qwen2.5:1.5b",
  "documents_count": 3,
  "chunks_count": 12,
  "components": {
    "api": "healthy",
    "vector_store": "healthy",
    "embeddings": "ready",
    "ollama": "healthy",
    "llm": "qwen2.5:1.5b"
  }
}
```

---

### `POST /query`
Executes RAG pipeline against indexed service documentation.

**Request Body**:
```json
{
  "question": "What should be checked when an EV reports repeated battery overheating?",
  "top_k": 5,
  "similarity_threshold": 0.35
}
```

**Response `200 OK`**:
```json
{
  "question": "What should be checked when an EV reports repeated battery overheating?",
  "answer": "Check coolant pump V54, check coolant level, inspect radiator for blockage, and verify temperature sensor readings.",
  "sources": [
    {
      "document": "sample_ev_battery_service.txt",
      "page": 1,
      "document_type": "TXT",
      "score": 0.82,
      "chunk_id": "sample_ev_battery_service.txt_p1_c0_a1b2c3",
      "snippet": "Check high-voltage battery cooling system..."
    }
  ],
  "grounding": "HIGH",
  "sources_count": 1
}
```

---

### `POST /feedback`
Records technician feedback for model answer quality.

**Request Body**:
```json
{
  "query": "What should be checked when an EV reports repeated battery overheating?",
  "answer": "Check coolant pump V54...",
  "helpful": true,
  "reason": "Accurate diagnostic steps",
  "comments": "Very helpful for technician."
}
```

**Response `200 OK`**:
```json
{
  "status": "success",
  "message": "Feedback recorded successfully."
}
```
