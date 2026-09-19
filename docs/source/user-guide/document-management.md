# Document Management & Deletion

Document management is handled in **Tab 2: Knowledge Base Dashboard**.

## Viewing Indexed Documents

The dashboard renders an overview table listing all currently indexed documentation files:
- **Filename**: Clean basename of the indexed document.
- **Document Type**: Format extension (`PDF`, `TXT`, `DOCX`, `CSV`).
- **Pages Count**: Total distinct pages indexed.
- **Total Chunks**: Total vector chunks stored in FAISS.
- **Status**: Current indexing state (`Indexed`).

## Single-Click Document Deletion

Technicians can delete documents cleanly from the vector index:

1. Locate the document row in **Tab 2: Knowledge Base Dashboard**.
2. Click **🗑️ Delete**.
3. A confirmation spinner will show deletion progress.
4. The system:
   - Identifies all vector chunks matching the target document identifier across metadata fields (`document_id`, `document`, `source`).
   - Removes matching chunks from the docstore.
   - Safely rebuilds the FAISS vector index from remaining documents.
   - Saves updated `index.faiss` and `index.pkl` files to disk.
   - Removes physical upload file from `data/uploads/` if present.
5. The UI automatically refreshes to reflect updated metrics.
6. Queries executed after deletion will no longer retrieve chunks from the deleted document.
