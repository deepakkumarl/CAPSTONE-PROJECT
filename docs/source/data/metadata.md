# Metadata Schemas

Detailed attributes stored across document, chunk, history, and feedback data structures.

## 1. Chunk Metadata Schema

```json
{
  "document_id": "sample_ev_battery_service.txt",
  "document": "sample_ev_battery_service.txt",
  "source": "sample_ev_battery_service.txt",
  "page": 1,
  "document_type": "TXT",
  "chunk_id": "sample_ev_battery_service.txt_p1_c0_a1b2c3"
}
```

## 2. Query History Entry Schema

```json
{
  "timestamp": "2026-09-19T14:30:00Z",
  "question": "What should be checked when an EV reports repeated battery overheating?",
  "answer": "Check coolant pump V54...",
  "retrieved_documents": ["sample_ev_battery_service.txt"],
  "sources_count": 1,
  "sources": [...],
  "status": "success"
}
```

## 3. Technician Feedback Schema

```json
{
  "timestamp": "2026-09-19T14:35:00Z",
  "query": "What should be checked when an EV reports repeated battery overheating?",
  "answer": "Check coolant pump V54...",
  "helpful": true,
  "reason": "Accurate diagnostic steps",
  "comments": "Very clear instructions."
}
```
