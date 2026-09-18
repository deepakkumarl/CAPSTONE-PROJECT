from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from src.ai.vector_store import VectorStoreManager
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("retriever")

class ServiceKnowledgeRetriever:
    """Retrieves relevant service document chunks from FAISS vector store with relevance thresholding."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager = None,
        top_k: int = settings.TOP_K,
        similarity_threshold: float = settings.SIMILARITY_THRESHOLD
    ):
        self.vector_store_manager = vector_store_manager or VectorStoreManager()
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query: str) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Retrieves relevant documents matching the query.
        Returns tuple of (relevant_documents, sources_metadata_list).
        If top score is below similarity threshold, returns empty lists.
        """
        if not query or not query.strip():
            logger.warning("Empty query provided to retriever.")
            return [], []

        results = self.vector_store_manager.similarity_search_with_score(
            query=query,
            top_k=self.top_k
        )

        if not results:
            logger.info("No documents found in vector store.")
            return [], []

        relevant_docs = []
        sources = []

        for doc, score in results:
            logger.info(f"Chunk from '{doc.metadata.get('source')}' score: {score:.4f} (threshold: {self.similarity_threshold})")
            if score >= self.similarity_threshold:
                relevant_docs.append(doc)
                sources.append({
                    "document": doc.metadata.get("source", "Unknown Document"),
                    "page": doc.metadata.get("page", 1),
                    "document_type": doc.metadata.get("document_type", "Text"),
                    "score": round(score, 4),
                    "chunk_id": doc.metadata.get("chunk_id", "")
                })

        if not relevant_docs:
            logger.info(f"No retrieved chunks met the similarity threshold ({self.similarity_threshold}).")
            return [], []

        logger.info(f"Retrieved {len(relevant_docs)} chunks passing relevance threshold.")
        return relevant_docs, sources
