# FAISS Vector Store Architecture

The vector index management system is implemented in `VectorStoreManager` (`src/ai/vector_store.py`).

## 1. Vector Store Index Design

- **Library**: FAISS (Facebook AI Similarity Search) CPU implementation.
- **Index Type**: Flat L2 Index (`IndexFlatL2`) wrapped inside LangChain `FAISS`.
- **Dimension**: 384 dimensions matching `sentence-transformers/all-MiniLM-L6-v2`.
- **Docstore**: `InMemoryDocstore` mapping UUID keys to `Document` objects containing text content and metadata dictionaries.

## 2. Disk Persistence Layout

Vector store state is persisted in `data/vectorstore/`:
- `index.faiss`: Binary FAISS vector index storing embedding float arrays.
- `index.pkl`: Pickled dictionary mapping internal FAISS vector IDs to docstore Document objects and metadata.

```bash
data/vectorstore/
├── index.faiss    # Binary vector index
└── index.pkl      # Pickled docstore metadata mapping
```

## 3. Chunk Deduplication Mechanism

When `add_documents()` is called:
1. `VectorStoreManager` inspects existing `chunk_id` values in `self.vector_store.docstore._dict`.
2. New document chunks whose `chunk_id` matches an existing ID in `existing_ids` are filtered out.
3. Only unique chunks are embedded and appended to the FAISS index, preventing vector duplication when ingesting the same document multiple times.
