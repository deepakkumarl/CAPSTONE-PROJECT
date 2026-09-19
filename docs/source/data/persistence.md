# Local Data Persistence

Persistence lifecycle for history, feedback, and FAISS index files.

## 1. JSON Persistence Managers
- **`QueryHistoryManager`** (`src/utils/history.py`): Manages atomic read/write operations for `data/query_history.json`. Limits total entries to 100 recent items.
- **`FeedbackManager`** (`src/utils/history.py`): Manages atomic read/write operations for `data/feedback.json`. Limits total entries to 200 recent feedback records.

## 2. FAISS Persistence (`VectorStoreManager.save`)
Applies atomic directory creation and calls `FAISS.save_local("data/vectorstore")` to synchronize in-memory vectors with disk files (`index.faiss`, `index.pkl`).
