# Knowledge Base Ingestion

Knowledge base ingestion converts raw multi-format files into searchable dense vector embeddings.

## Automated Bulk Ingestion

The platform comes pre-seeded with sample BMW service documentation located in `data/sample/`:
- `sample_charging_system.txt`: EV charging port diagnostic routines, CP & PP signal verification steps.
- `sample_ev_battery_service.txt`: High-voltage battery overheating diagnostics, coolant pump V54 checks.
- `sample_thermal_management.txt`: Cooling circuit component verification and valve inspection steps.

### Triggering Sample Ingestion via UI
In **Tab 2: Knowledge Base Dashboard**, click **Re-index Sample Knowledge Base Directory** to scan `data/sample/` and ingest all files into the FAISS index.

### Triggering Ingestion via REST API
```bash
curl -X POST http://localhost:8000/ingest
```

## Ingestion Pipeline Steps
1. **Directory Scanning**: Scans target directory for files matching supported extensions (`.pdf`, `.txt`, `.docx`, `.csv`).
2. **Text Cleaning**: Normalizes line endings (`\r\n` -> `\n`), strips control characters, and collapses whitespace.
3. **Recursive Chunking**: Splits text into 800-character segments with 100-character overlap.
4. **Metadata Enrichment**: Assigns `document_id`, `source`, `page`, `document_type`, and a unique `chunk_id`.
5. **Deduplication Check**: Skips chunks whose `chunk_id` already exists in the FAISS docstore.
6. **Dense Embedding**: Encodes unique chunks into 384-dimensional vectors using `all-MiniLM-L6-v2`.
7. **FAISS Indexing & Persistence**: Adds vectors to FAISS index and saves `index.faiss` and `index.pkl` to disk.
