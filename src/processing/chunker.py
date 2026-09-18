import uuid
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("chunker")

class DocumentChunker:
    """Split documents into configurable text chunks with rich metadata."""

    def __init__(self, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", "; ", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits a list of LangChain Document objects into smaller chunks,
        preserving and enriching metadata with unique chunk_id.
        """
        if not documents:
            logger.warning("No documents passed to chunker.")
            return []

        chunks = self.splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} raw document sections into {len(chunks)} text chunks.")

        for idx, chunk in enumerate(chunks):
            # Ensure metadata dictionary exists
            if not isinstance(chunk.metadata, dict):
                chunk.metadata = {}

            source_file = chunk.metadata.get("source", "unknown")
            page_num = chunk.metadata.get("page", 1)
            doc_type = chunk.metadata.get("document_type", "text")

            # Assign unique chunk_id
            chunk_id = f"{source_file}_p{page_num}_c{idx}_{uuid.uuid4().hex[:6]}"
            chunk.metadata["chunk_id"] = chunk_id
            chunk.metadata["source"] = source_file
            chunk.metadata["page"] = page_num
            chunk.metadata["document_type"] = doc_type

        return chunks
