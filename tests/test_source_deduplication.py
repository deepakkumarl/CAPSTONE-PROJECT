import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document
from src.ai.retriever import ServiceKnowledgeRetriever

def test_source_deduplication():
    mock_vs = MagicMock()

    doc1 = Document(
        page_content="Coolant pump V54 diagnostic check procedure step 1.",
        metadata={"source": "sample_ev_battery_service.txt", "page": 1, "chunk_id": "c1", "document_type": "TXT"}
    )
    doc2 = Document(
        page_content="Coolant pump V54 diagnostic check procedure step 2.",
        metadata={"source": "sample_ev_battery_service.txt", "page": 1, "chunk_id": "c1", "document_type": "TXT"}
    )

    # Return duplicate-looking chunks with different raw L2 distances
    mock_vs.similarity_search_with_score.return_value = [
        (doc1, 0.88),
        (doc2, 0.85)
    ]

    retriever = ServiceKnowledgeRetriever(vector_store_manager=mock_vs, similarity_threshold=0.35)
    docs, sources = retriever.retrieve("coolant pump V54")

    # Sources list should contain unique entries (deduplicated by chunk_id / document+page)
    assert len(sources) == 1
    assert sources[0]["document"] == "sample_ev_battery_service.txt"
    assert sources[0]["page"] == 1
    assert sources[0]["score"] == 0.88
