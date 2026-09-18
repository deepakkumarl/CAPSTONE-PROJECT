from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.ai.embeddings import get_embeddings
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("vector_store")

class VectorStoreManager:
    """Manages creation, loading, persistence, deduplication, and document deletion for FAISS index."""

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
                logger.info(f"FAISS vector store loaded successfully with {self.get_total_chunks_count()} chunks.")
            except Exception as e:
                logger.error(f"Failed to load existing FAISS index: {e}")
                self.vector_store = None
        else:
            logger.info("No existing FAISS index found. A new store will be created upon document ingestion.")

    def get_total_chunks_count(self) -> int:
        """Returns the total number of vector chunks stored in FAISS."""
        if self.vector_store is None:
            return 0
        try:
            return len(self.vector_store.docstore._dict)
        except Exception:
            return 0

    def add_documents(self, documents: List[Document]) -> int:
        """
        Adds new document chunks to the FAISS vector store.
        Deduplicates chunks based on chunk_id.
        """
        if not documents:
            logger.warning("No documents provided to add_documents.")
            return 0

        existing_ids = set()
        if self.vector_store is not None:
            try:
                for doc_id, doc in self.vector_store.docstore._dict.items():
                    c_id = doc.metadata.get("chunk_id")
                    if c_id:
                        existing_ids.add(c_id)
            except Exception:
                pass

        new_docs = []
        for doc in documents:
            c_id = doc.metadata.get("chunk_id")
            if c_id and c_id in existing_ids:
                continue
            new_docs.append(doc)

        if not new_docs:
            logger.info("All provided document chunks already exist in vector index. Skipping addition.")
            return 0

        logger.info(f"Adding {len(new_docs)} new document chunks to FAISS index...")
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(new_docs, self.embeddings)
        else:
            self.vector_store.add_documents(new_docs)

        logger.info(f"Successfully added {len(new_docs)} chunks to FAISS index.")
        return len(new_docs)

    def save(self):
        """Persists the FAISS vector store to disk."""
        if self.vector_store is not None:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(self.persist_dir))
            logger.info(f"Saved FAISS index to {self.persist_dir}")

    def delete_document(self, document_identifier: str) -> Tuple[bool, int, str]:
        """
        Deletes all vector chunks associated with a specific document identifier (basename).
        Safely rebuilds the FAISS index from remaining documents and persists to disk.
        Returns tuple of (success: bool, chunks_removed: int, target_filename: str).
        """
        if self.vector_store is None:
            logger.warning("Cannot delete document: vector store is empty.")
            return False, 0, document_identifier

        target_name = Path(document_identifier).name

        try:
            remaining_docs = []
            deleted_count = 0

            for doc_id, doc in list(self.vector_store.docstore._dict.items()):
                # Extract clean basenames from all candidate metadata attributes
                meta_doc_id = Path(str(doc.metadata.get("document_id", ""))).name
                meta_document = Path(str(doc.metadata.get("document", ""))).name
                meta_source = Path(str(doc.metadata.get("source", ""))).name

                if target_name in (meta_doc_id, meta_document, meta_source):
                    deleted_count += 1
                else:
                    remaining_docs.append(doc)

            if deleted_count == 0:
                logger.warning(f"No indexed chunks found for document '{target_name}'")
                return False, 0, target_name

            logger.info(f"Deleting {deleted_count} chunks for document '{target_name}'. Rebuilding FAISS index...")

            if remaining_docs:
                self.vector_store = FAISS.from_documents(remaining_docs, self.embeddings)
                self.save()
            else:
                self.vector_store = None
                index_file = self.persist_dir / "index.faiss"
                pkl_file = self.persist_dir / "index.pkl"
                if index_file.exists():
                    index_file.unlink()
                if pkl_file.exists():
                    pkl_file.unlink()
                logger.info("Vector store is now empty after document deletion.")

            # Also delete physical file from uploads if present
            upload_path = settings.DATA_UPLOAD_DIR / target_name
            if upload_path.exists():
                upload_path.unlink()
                logger.info(f"Removed uploaded file from disk: {upload_path}")

            return True, deleted_count, target_name

        except Exception as e:
            logger.error(f"Error deleting document '{target_name}': {e}")
            return False, 0, target_name

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
            docstore = self.vector_store.docstore
            for doc_id, doc in docstore._dict.items():
                raw_source = doc.metadata.get("document_id") or doc.metadata.get("document") or doc.metadata.get("source") or "unknown"
                source_name = Path(str(raw_source)).name
                doc_type = doc.metadata.get("document_type", "unknown")
                page = doc.metadata.get("page", 1)

                if source_name not in doc_summary:
                    doc_summary[source_name] = {
                        "filename": source_name,
                        "document_type": doc_type,
                        "total_chunks": 0,
                        "pages": set(),
                        "status": "Indexed"
                    }
                doc_summary[source_name]["total_chunks"] += 1
                doc_summary[source_name]["pages"].add(page)

            result = []
            for k, v in doc_summary.items():
                result.append({
                    "filename": v["filename"],
                    "document_type": v["document_type"],
                    "total_chunks": v["total_chunks"],
                    "pages_count": len(v["pages"]),
                    "status": v["status"]
                })
            return result
        except Exception as e:
            logger.error(f"Error reading indexed documents info: {e}")
            return []
