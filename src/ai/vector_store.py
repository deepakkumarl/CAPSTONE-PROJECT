from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.ai.embeddings import get_embeddings
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("vector_store")

class VectorStoreManager:
    """Manages creation, loading, persistence, and similarity search for FAISS vector index."""

    def __init__(self, persist_dir: Path = settings.VECTORSTORE_DIR):
        self.persist_dir = Path(persist_dir)
        self.embeddings = get_embeddings()
        self.vector_store: Optional[FAISS] = None
        self._load_or_init()

    def _load_or_init(self):
        """Loads existing FAISS index from disk if available."""
        index_file = self.persist_dir / "index.faiss"
        if index_file.exists():
            try:
                logger.info(f"Loading existing FAISS index from {self.persist_dir}")
                self.vector_store = FAISS.load_local(
                    folder_path=str(self.persist_dir),
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("FAISS vector store loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load existing FAISS index: {e}")
                self.vector_store = None
        else:
            logger.info("No existing FAISS index found. A new store will be created upon document ingestion.")

    def add_documents(self, documents: List[Document]) -> int:
        """Adds new documents to the FAISS vector store."""
        if not documents:
            logger.warning("No documents provided to add_documents.")
            return 0

        logger.info(f"Adding {len(documents)} document chunks to FAISS...")
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)

        logger.info(f"Successfully added {len(documents)} chunks to FAISS index.")
        return len(documents)

    def save(self):
        """Persists the FAISS vector store to disk."""
        if self.vector_store is not None:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(self.persist_dir))
            logger.info(f"Saved FAISS index to {self.persist_dir}")

    def similarity_search_with_score(
        self, query: str, top_k: int = settings.TOP_K
    ) -> List[Tuple[Document, float]]:
        """
        Performs similarity search and returns (Document, normalized_similarity_score) tuples.
        Score is normalized to range [0.0, 1.0] where 1.0 is highest relevance.
        """
        if self.vector_store is None:
            logger.warning("Vector store is not initialized or contains no documents.")
            return []

        try:
            results = self.vector_store.similarity_search_with_score(query, k=top_k)
            scored_docs = []
            for doc, raw_score in results:
                # FAISS score for L2 distance: lower distance = higher similarity.
                # Normalized similarity conversion:
                sim_score = max(0.0, min(1.0, 1.0 - (float(raw_score) / 2.0)))
                scored_docs.append((doc, sim_score))

            logger.info(f"Retrieved {len(scored_docs)} candidate chunks for query: '{query[:40]}...'")
            return scored_docs
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            return []

    def get_indexed_documents_info(self) -> List[Dict[str, Any]]:
        """Returns metadata summary of currently indexed documents."""
        if self.vector_store is None:
            return []

        doc_summary = {}
        try:
            # Access underlying docstore
            docstore = self.vector_store.docstore
            for doc_id, doc in docstore._dict.items():
                source = doc.metadata.get("source", "unknown")
                doc_type = doc.metadata.get("document_type", "unknown")
                page = doc.metadata.get("page", 1)

                if source not in doc_summary:
                    doc_summary[source] = {
                        "filename": source,
                        "document_type": doc_type,
                        "total_chunks": 0,
                        "pages": set()
                    }
                doc_summary[source]["total_chunks"] += 1
                doc_summary[source]["pages"].add(page)

            result = []
            for k, v in doc_summary.items():
                result.append({
                    "filename": v["filename"],
                    "document_type": v["document_type"],
                    "total_chunks": v["total_chunks"],
                    "pages_count": len(v["pages"])
                })
            return result
        except Exception as e:
            logger.error(f"Error reading indexed documents info: {e}")
            return []
