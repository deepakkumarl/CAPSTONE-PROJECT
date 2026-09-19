# Configuration Reference

The platform uses Pydantic BaseSettings in `src/utils/config.py` to manage application parameters and environment variables.

## Environment Variables

| Variable | Description | Default Value | Example |
| :--- | :--- | :--- | :--- |
| `OLLAMA_BASE_URL` | Base URL of local Ollama server | `http://localhost:11434` | `http://host.docker.internal:11434` |
| `OLLAMA_MODEL` | Target Ollama LLM model | `qwen2.5:1.5b` | `qwen2.5:1.5b` |
| `EMBEDDING_MODEL` | HuggingFace embedding model name | `sentence-transformers/all-MiniLM-L6-v2` | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOP_K` | Default number of vector chunks to retrieve | `5` | `5` |
| `SIMILARITY_THRESHOLD` | Minimum score threshold for chunk retrieval | `0.35` | `0.35` |
| `CHUNK_SIZE` | Text chunk character size | `800` | `800` |
| `CHUNK_OVERLAP` | Character overlap between consecutive chunks | `100` | `100` |
| `BACKEND_URL` | FastAPI backend URL used by Streamlit | `http://localhost:8000` | `http://backend:8000` |
| `EVALUATION_TIMEOUT` | Timeout limit per benchmark test case (seconds) | `35` | `35` |
| `VECTORSTORE_DIR` | Relative path to store FAISS vector index files | `data/vectorstore` | `data/vectorstore` |
| `DATA_SAMPLE_DIR` | Relative path to sample document directory | `data/sample` | `data/sample` |
| `DATA_UPLOAD_DIR` | Relative path to save uploaded documents | `data/uploads` | `data/uploads` |
| `HISTORY_FILE_PATH` | Path to query history JSON file | `data/query_history.json` | `data/query_history.json` |
| `FEEDBACK_FILE_PATH` | Path to user feedback JSON file | `data/feedback.json` | `data/feedback.json` |

## `.env` File Example

Create a `.env` file in the root directory to override default settings:

```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=5
SIMILARITY_THRESHOLD=0.35
CHUNK_SIZE=800
CHUNK_OVERLAP=100
BACKEND_URL=http://localhost:8000
```
