from typing import List, Dict, Any, Tuple, Optional
from langchain_core.documents import Document
from src.ai.vector_store import VectorStoreManager
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("retriever")

class ServiceKnowledgeRetriever:
    """Retrieves relevant service document chunks from FAISS vector store with relevance thresholding and source deduplication."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager = None,
        top_k: int = settings.TOP_K,
        similarity_threshold: float = settings.SIMILARITY_THRESHOLD
    ):
        self.vector_store_manager = vector_store_manager or VectorStoreManager()
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None
    ) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Retrieves relevant documents matching the query.
        Returns tuple of (relevant_documents, unique_sources_metadata_list).
        Deduplicates sources by (document, page) and chunk_id keeping highest similarity score.
        If top score is below similarity threshold, returns empty lists.
        """
        if not query or not query.strip():
            logger.warning("Empty query provided to retriever.")
            return [], []

        k = top_k if top_k is not None else self.top_k
        thresh = similarity_threshold if similarity_threshold is not None else self.similarity_threshold

        results = self.vector_store_manager.similarity_search_with_score(
            query=query,
            top_k=k
        )

        if not results:
            logger.info("No documents found in vector store.")
            return [], []

        relevant_docs = []
        sources_dict = {}

        for doc, score in results:
            logger.info(f"Chunk from '{doc.metadata.get('source')}' score: {score:.4f} (threshold: {thresh})")
            if score >= thresh:
                relevant_docs.append(doc)
                source_name = doc.metadata.get("source", "Unknown Document")
                page_num = doc.metadata.get("page", 1)
                chunk_id = doc.metadata.get("chunk_id", "")
                doc_type = doc.metadata.get("document_type", "Text")

                # Unique key based on (document, page) and chunk_id for strict deduplication
                dedup_key = f"{source_name}_p{page_num}_{chunk_id}"

                if dedup_key not in sources_dict or score > sources_dict[dedup_key]["score"]:
                    sources_dict[dedup_key] = {
                        "document": source_name,
                        "page": page_num,
                        "document_type": doc_type,
                        "score": round(score, 4),
                        "chunk_id": chunk_id,
                        "snippet": doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                    }

        if not relevant_docs:
            logger.info(f"No retrieved chunks met the similarity threshold ({thresh}).")
            return [], []

        unique_sources = sorted(list(sources_dict.values()), key=lambda x: x["score"], reverse=True)

        logger.info(f"Retrieved {len(relevant_docs)} chunks passing threshold. Deduplicated into {len(unique_sources)} unique sources.")
        return relevant_docs, unique_sources
