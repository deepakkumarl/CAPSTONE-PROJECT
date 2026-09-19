# `GET /health` — Component Health Monitoring

Returns live structured operational status for API router, vector store, embedding model, and local Ollama LLM connection.

## HTTP Request
`GET /health`

## Query Parameters
None.

## Response Model (`HealthResponse`)

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `status` | String | API health contract status | `"ok"` |
| `api` | String | FastAPI router operational state | `"healthy"` |
| `vector_store` | String | FAISS index status | `"ready"` or `"no_index"` |
| `embeddings` | String | SentenceTransformers state | `"ready"` or `"unavailable"` |
| `ollama` | String | Local Ollama connection state | `"connected"` or `"disconnected"` |
| `llm` | String | Target Ollama model name | `"qwen2.5:1.5b"` |
| `documents_count` | Integer | Total distinct documents indexed | `3` |
| `chunks_count` | Integer | Total vector chunks in index | `12` |
| `components` | Dict[String, String] | Component-level health mapping | `{"api": "healthy", ...}` |

## Example Response JSON
```json
{
  "status": "ok",
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

## Example `curl` Command
```bash
curl -X GET http://localhost:8000/health
```
