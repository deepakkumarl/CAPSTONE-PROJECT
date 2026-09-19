# Security Scanning & AST Tools

The project uses **Bandit** for AST static security analysis.

## Running Bandit Locally

```bash
bandit -r src
```

## Bandit Justifications & Annotations

- **B104 (`0.0.0.0` Host Binding in `src/api/main.py`)**: Annotated with `# nosec B104`. Binding `0.0.0.0` is required for Docker multi-container networking so that Streamlit and external HTTP callers can reach the FastAPI Uvicorn process inside the container.
- **B110 (`try/except/pass` in `src/ai/vector_store.py`)**: Resolved by replacing silent `pass` blocks with explicit `logger.warning(...)` logging.
