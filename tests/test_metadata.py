import pytest
from langchain_core.documents import Document
from src.processing.chunker import DocumentChunker

def test_chunk_metadata_preservation():
    doc = Document(
        page_content="High voltage battery cell temperature sensor reading diagnostic.",
        metadata={"source": "sample_ev_battery_service.txt", "page": 3, "document_type": "TXT"}
    )

    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    chunks = chunker.split_documents([doc])

    assert len(chunks) == 1
    c = chunks[0]
    assert c.metadata["source"] == "sample_ev_battery_service.txt"
    assert c.metadata["page"] == 3
    assert c.metadata["document_type"] == "TXT"
    assert "chunk_id" in c.metadata
