# Data & Storage Overview

The platform uses a lightweight, 100% file-based local storage architecture avoiding complex database administration.

## Storage Locations Summary

| Data Asset | Path | File Format | Description |
| :--- | :--- | :--- | :--- |
| **Sample Knowledge Base** | `data/sample/` | `.txt`, `.pdf`, `.docx`, `.csv` | Pre-seeded service documentation |
| **Uploaded Documents** | `data/uploads/` | Multi-format files | User uploaded documentation |
| **FAISS Vector Index** | `data/vectorstore/index.faiss` | Binary FAISS file | 384-dimensional dense vectors |
| **FAISS Docstore Map** | `data/vectorstore/index.pkl` | Pickled Python dict | Document content & metadata |
| **Query History** | `data/query_history.json` | JSON Array | Audit log of technician queries |
| **Technician Feedback** | `data/feedback.json` | JSON Array | Thumbs up/down feedback records |
