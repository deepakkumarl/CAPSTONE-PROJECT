# `POST /ingest` — Sample Directory Ingestion

Scans the sample data directory (`data/sample/`) and ingests all valid documentation files into the FAISS vector store.

## HTTP Request
`POST /ingest`

## Request Body
None.

## Response Model (`IngestResponse`)
```json
{
  "status": "success",
  "message": "Successfully ingested 3 file(s) into 12 vector chunks.",
  "documents_count": 3,
  "chunks_count": 12
}
```

## Example `curl` Command
```bash
curl -X POST http://localhost:8000/ingest
```
