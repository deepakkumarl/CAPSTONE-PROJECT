import os
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings  # fallback compatibility


class Settings(BaseSettings):
    """Application Configuration Settings."""

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    TOP_K: int = int(os.getenv("TOP_K", "4"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    VECTORSTORE_DIR: Path = BASE_DIR / os.getenv("VECTORSTORE_DIR", "data/vectorstore")
    DATA_SAMPLE_DIR: Path = BASE_DIR / os.getenv("DATA_SAMPLE_DIR", "data/sample")
    DATA_UPLOAD_DIR: Path = BASE_DIR / os.getenv("DATA_UPLOAD_DIR", "data/uploads")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Ensure directories exist
settings.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
