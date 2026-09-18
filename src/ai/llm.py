from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("llm")

def get_llm():
    """
    Instantiates and returns the local Ollama LLM wrapper.
    Model: qwen2.5:1.5b
    Base URL: http://localhost:11434 (configurable)
    """
    model_name = settings.OLLAMA_MODEL
    base_url = settings.OLLAMA_BASE_URL
    logger.info(f"Connecting to local Ollama LLM model '{model_name}' at base URL '{base_url}'")

    try:
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.0
        )
    except ImportError:
        logger.warning("langchain_ollama not installed, falling back to langchain_community.chat_models.ChatOllama")
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.0
        )
