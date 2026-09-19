# `POST /upload` — Document Upload & Ingestion

Uploads a single multi-format document (`.pdf`, `.txt`, `.docx`, `.csv`), saves it to `data/uploads/`, and indexes its contents into the FAISS vector store.

## HTTP Request
`POST /upload`

## Request Payload
- **Content-Type**: `multipart/form-data`
- **Body Field**: `file` (UploadFile binary content)

## Allowed File Extensions
- `.pdf`, `.txt`, `.docx`, `.csv`

## Validation Rules & HTTP Errors
- **`400 Bad Request`**: File extension not in allowed set.
- **`400 Bad Request`**: Filename contains path traversal elements (`..`, `/`, `\`) or empty name.
- **`400 Bad Request`**: File size exceeds 10 MB maximum limit.
- **`400 Bad Request`**: Uploaded file is empty (0 bytes).

## Response Model (`IngestResponse`)
```json
{
  "status": "success",
  "message": "Successfully ingested 'sample_ev_battery_service.txt' into 4 vector chunks.",
  "documents_count": 1,
  "chunks_count": 4
}
```

## Example `curl` Command
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/sample_ev_battery_service.txt"
```
