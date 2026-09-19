# `POST /query` — Diagnostic Query Execution

Submits a technical service question to the RAG pipeline and returns a grounded LLM answer along with deduplicated source metadata citations.

## HTTP Request
`POST /query`

## Request Model (`QueryRequest`)

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `question` | String | Yes | Diagnostic question | `"What should be checked when an EV reports repeated battery overheating?"` |
| `top_k` | Integer | No | Chunks to retrieve (1-20) | `5` |
| `similarity_threshold` | Float | No | Relevance threshold (0.0-1.0) | `0.35` |

## Response Model (`QueryResponse`)

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `question` | String | Original question | `"What should be checked..."` |
| `answer` | String | Grounded LLM response | `"Check coolant pump V54..."` |
| `sources` | List[SourceMetadata] | Deduplicated sources | `[...]` |
| `grounding` | String | Grounding assessment | `"HIGH"`, `"MEDIUM"`, `"INSUFFICIENT"` |
| `sources_count` | Integer | Number of sources | `1` |

## Example Request JSON
```json
{
  "question": "What should be checked when an EV reports repeated battery overheating?",
  "top_k": 5,
  "similarity_threshold": 0.35
}
```

## Example Response JSON
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

## Example `curl` Command
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What should be checked when an EV reports repeated battery overheating?",
    "top_k": 5,
    "similarity_threshold": 0.35
  }'
```
