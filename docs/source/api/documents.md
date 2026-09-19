# `GET /documents` & `DELETE /documents/{filename}`

Endpoints for listing and deleting indexed documents from the FAISS vector store.

---

## 1. List Documents: `GET /documents`

Returns a list of all documents currently indexed in the FAISS vector index along with page and chunk count summary.

### Response Model (`DocumentListResponse`)
```json
{
  "documents": [
    {
      "filename": "sample_ev_battery_service.txt",
      "document_type": "TXT",
      "total_chunks": 4,
      "pages_count": 1,
      "status": "Indexed"
    },
    {
      "filename": "sample_charging_system.txt",
      "document_type": "TXT",
      "total_chunks": 4,
      "pages_count": 1,
      "status": "Indexed"
    }
  ],
  "total_indexed_documents": 2
}
```

### Example `curl` Command
```bash
curl -X GET http://localhost:8000/documents
```

---

## 2. Delete Document: `DELETE /documents/{filename}`

Deletes all vector chunks associated with target document filename and safely rebuilds the FAISS index.

### Path Parameter
- `filename`: Clean document filename basename (e.g., `sample_ev_battery_service.txt`).

### Response Model (`DeleteDocumentResponse`)
```json
{
  "status": "success",
  "message": "Document 'sample_ev_battery_service.txt' deleted successfully.",
  "document": "sample_ev_battery_service.txt",
  "chunks_removed": 4
}
```

### Error Responses
- **`404 Not Found`**: Document filename not found in vector store docstore.

### Example `curl` Command
```bash
curl -X DELETE http://localhost:8000/documents/sample_ev_battery_service.txt
```
