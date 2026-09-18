from pathlib import Path
from typing import Dict, Any, List
from src.ingestion.document_loader import load_documents_from_dir, load_single_document
from src.processing.chunker import DocumentChunker
from src.ai.vector_store import VectorStoreManager
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("ingest")

class IngestionPipeline:
    """Orchestrates document loading, text cleaning, chunking, and FAISS indexing."""

    def __init__(self, vector_store_manager: VectorStoreManager = None):
        self.vector_store_manager = vector_store_manager or VectorStoreManager()
        self.chunker = DocumentChunker(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def run(self, source_dir: Path = settings.DATA_SAMPLE_DIR) -> Dict[str, Any]:
        """
        Runs the full ingestion pipeline on documents in the source directory.
        """
        source_dir = Path(source_dir)
        logger.info(f"Starting ingestion pipeline from: {source_dir}")

        raw_docs = load_documents_from_dir(source_dir)
        if not raw_docs:
            logger.warning(f"No documents found to ingest in {source_dir}")
            return {
                "status": "warning",
                "message": f"No valid documents found in {source_dir}",
                "documents_count": 0,
                "chunks_count": 0
            }

        chunks = self.chunker.split_documents(raw_docs)
        if not chunks:
            logger.warning("No text chunks generated.")
            return {
                "status": "warning",
                "message": "Failed to split documents into chunks.",
                "documents_count": len(raw_docs),
                "chunks_count": 0
            }

        # Index chunks into FAISS vector store
        indexed_count = self.vector_store_manager.add_documents(chunks)
        self.vector_store_manager.save()

        unique_filenames = list(set([doc.metadata.get("source", "unknown") for doc in raw_docs]))

        logger.info(f"Ingestion completed. Files: {len(unique_filenames)}, Chunks: {indexed_count}")
        return {
            "status": "success",
            "message": f"Successfully ingested {len(unique_filenames)} file(s) into {indexed_count} vector chunks.",
            "documents_count": len(unique_filenames),
            "filenames": unique_filenames,
            "chunks_count": indexed_count
        }

    def ingest_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Ingests a single uploaded file into the vector store."""
        file_path = Path(file_path)
        logger.info(f"Ingesting single file: {file_path}")

        raw_docs = load_single_document(file_path)
        if not raw_docs:
            return {
                "status": "error",
                "message": f"Failed to load content from file {file_path.name}",
                "chunks_count": 0
            }

        chunks = self.chunker.split_documents(raw_docs)
        indexed_count = self.vector_store_manager.add_documents(chunks)
        self.vector_store_manager.save()

        return {
            "status": "success",
            "message": f"Successfully ingested '{file_path.name}' into {indexed_count} vector chunks.",
            "filename": file_path.name,
            "chunks_count": indexed_count
        }
