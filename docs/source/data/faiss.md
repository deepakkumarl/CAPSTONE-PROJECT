# FAISS Vector Index Specifications

Specifications for the local FAISS index implementation.

## Index Properties

- **Metric**: L2 Euclidean Distance
- **Vector Space**: 384 dimensions (`all-MiniLM-L6-v2`)
- **Deserialization Security**: `allow_dangerous_deserialization=True` explicitly enabled for local trusted index loading.
- **Index Rebuilding**: When a document is deleted via `DELETE /documents/{filename}`, `VectorStoreManager` extracts remaining un-deleted chunks from `docstore._dict`, re-creates the `FAISS` index via `FAISS.from_documents()`, and overwrites `index.faiss` and `index.pkl`.
