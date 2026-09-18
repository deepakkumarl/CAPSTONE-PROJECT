from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("embeddings")

def get_embeddings():
    """
    Instantiates and returns the local HuggingFace embeddings model.
    Uses 'sentence-transformers/all-MiniLM-L6-v2' by default.
    """
    model_name = settings.EMBEDDING_MODEL
    logger.info(f"Initializing local embeddings model: {model_name}")

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
    except ImportError:
        logger.warning("langchain_huggingface not available, falling back to langchain_community.embeddings")
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
