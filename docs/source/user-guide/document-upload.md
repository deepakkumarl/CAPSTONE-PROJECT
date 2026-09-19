# Document Upload

Technicians can upload new technical documentation directly into the knowledge base through the Streamlit sidebar or the REST API.

## Supported File Formats
- **PDF (`.pdf`)**: Technical manuals, electrical schematics, service bulletins.
- **Text (`.txt`)**: Plain text diagnostic procedures and release notes.
- **Word (`.docx`)**: Workshop repair guides and standard operating procedures.
- **CSV (`.csv`)**: Fault code tables, diagnostic trouble code (DTC) lists, torque specs.

## How to Upload via Streamlit UI

1. Open the **Sidebar Document Management** section on the left panel.
2. Click **Browse files** or drag and drop document files.
3. Supported formats are automatically filtered (`.pdf`, `.txt`, `.docx`, `.csv`).
4. Click **Ingest Uploaded File(s)**.
5. A loading spinner will indicate file processing, text extraction, chunking, and FAISS vector indexing.
6. Upon completion, a success notification will confirm the number of chunks added, and the Knowledge Base metrics will update automatically.

## Upload Rules & Constraints
- **Maximum File Size**: 10 MB per file.
- **Filename Sanitization**: Path traversal characters (`..`, `/`, `\`) are stripped automatically.
- **Empty Files**: 0-byte uploads are rejected with a clear error message.
