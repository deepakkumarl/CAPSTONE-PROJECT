import pytest
from langchain_core.documents import Document
from src.processing.chunker import DocumentChunker

def test_document_chunker_split():
    long_text = "BMW Service Diagnostic Procedure. " * 50
    doc = Document(
        page_content=long_text,
        metadata={"source": "test_doc.pdf", "page": 1, "document_type": "PDF"}
    )

    chunker = DocumentChunker(chunk_size=200, chunk_overlap=20)
    chunks = chunker.split_documents([doc])

    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.page_content) <= 220
        assert chunk.metadata["source"] == "test_doc.pdf"
        assert "chunk_id" in chunk.metadata

def test_document_chunker_empty():
    chunker = DocumentChunker()
    assert chunker.split_documents([]) == []
