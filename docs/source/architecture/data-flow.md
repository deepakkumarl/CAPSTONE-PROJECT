# Data Flow Architecture

This document describes the primary data flows across document ingestion, query execution, document deletion, and technician feedback.

## 1. Document Ingestion Flow

```
File Upload / Sample Directory
           │
           v
+-------------------------------+
| Document Loader               |  (Extract text by format: PDF, TXT, DOCX, CSV)
+-------------------------------+
           │
           v
+-------------------------------+
| Text Cleaner                  |  (Normalize whitespace, strip non-printable chars)
+-------------------------------+
           │
           v
+-------------------------------+
| Chunker                       |  (800 char chunk size, 100 char overlap)
+-------------------------------+  (Enrich metadata: document_id, page, chunk_id)
           │
           v
+-------------------------------+
| VectorStoreManager            |  (Check chunk_id deduplication set)
| - Embeddings Generation       |  (Generate 384-dim vectors via MiniLM-L6-v2)
| - FAISS Add & Persist         |  (Save index.faiss and index.pkl to disk)
+-------------------------------+
```

## 2. Query Execution & History Flow

```
Technician Query -> FastAPI /query -> Retriever -> FAISS Vector Search
                                                         │
                                                         v
Technician UI <- FastAPI Response <- RAG Pipeline <- Context Chunks
                                         │
                                         v
                              QueryHistoryManager -> data/query_history.json
```

## 3. Document Deletion Flow

```
DELETE /documents/{filename}
           │
           v
VectorStoreManager.delete_document()
           │
           ├─ Iterates docstore._dict to identify matching chunks by document_id/source
           ├─ Filters out matching chunks and collects remaining Document objects
           ├─ If remaining documents exist:
           │     Rebuilds FAISS index via FAISS.from_documents()
           │     Persists new index.faiss and index.pkl to disk
           └─ If remaining documents is empty:
                 Removes index files and resets vector_store to None
```
