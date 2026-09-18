import pytest
from unittest.mock import MagicMock
from src.ai.rag import RAGPipeline, FALLBACK_RESPONSE
from langchain_core.documents import Document

def test_rag_fallback_on_empty_retrieval():
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = ([], [])

    pipeline = RAGPipeline(retriever=mock_retriever)
    result = pipeline.answer_question("How do I fix unknown fault code X9999?")

    assert result["answer"] == FALLBACK_RESPONSE
    assert result["sources"] == []
    mock_retriever.retrieve.assert_called_once_with("How do I fix unknown fault code X9999?")

def test_rag_formatting_with_retrieved_docs():
    mock_retriever = MagicMock()
    doc = Document(
        page_content="Inspect coolant pump V54 for cavitation noise.",
        metadata={"source": "sample_ev_battery_service.txt", "page": 1}
    )
    sources = [{
        "document": "sample_ev_battery_service.txt",
        "page": 1,
        "score": 0.89,
        "chunk_id": "chunk_1"
    }]
    mock_retriever.retrieve.return_value = ([doc], sources)

    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "The technician should inspect coolant pump V54 for cavitation noise."

    pipeline = RAGPipeline(retriever=mock_retriever)
    pipeline.llm = mock_llm

    result = pipeline.answer_question("What should be checked for coolant pump?")

    assert "coolant pump V54" in result["answer"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["document"] == "sample_ev_battery_service.txt"
