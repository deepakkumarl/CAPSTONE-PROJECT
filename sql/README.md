# SQL & Relational Metadata Storage

This project currently uses **FAISS (Facebook AI Similarity Search)** for high-performance in-memory vector storage and similarity search, persisted locally under `data/vectorstore/`.

A relational SQL database is not required for core vector retrieval. This `sql/` directory is reserved for future enterprise extensions, such as:
1. User authentication & role-based access control (RBAC)
2. Service query audit logs and technician feedback tracking
3. Document versioning, metadata history, and ingestion status tracking

### Schema Reservation Example (PostgreSQL / SQLite)
```sql
CREATE TABLE query_audit_logs (
    query_id UUID PRIMARY KEY,
    user_id VARCHAR(50),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
