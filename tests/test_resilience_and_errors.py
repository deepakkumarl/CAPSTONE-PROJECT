import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api.main import app
from src.ai.rag import RAGPipeline, FALLBACK_RESPONSE
from src.ai.vector_store import VectorStoreManager

client = TestClient(app)


def test_ollama_unavailable_graceful_handling():
    """Test that if Ollama fails/times out, RAG pipeline returns an error message instead of crashing."""
    pipeline = RAGPipeline()
    with patch.object(pipeline, "_init_llm"):
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("Ollama connection refused (http://localhost:11434)")
        pipeline.llm = mock_llm

        with patch.object(pipeline.retriever, "retrieve") as mock_retrieve:
            mock_doc = MagicMock()
            mock_doc.page_content = "Some context"
            mock_doc.metadata = {"source": "test.txt", "page": 1}
            mock_retrieve.return_value = ([mock_doc], [{"document": "test.txt", "page": 1, "score": 0.85}])

            res = pipeline.answer_question("What is the battery voltage?")
            assert "Error communicating with local LLM" in res["answer"]
            assert res["sources_count"] == 1


def test_path_traversal_upload_rejection():
    """Test path traversal attempt in file upload is rejected with 400 Bad Request."""
    files = {"file": ("../../etc/passwd.txt", b"malicious content", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Invalid or malicious filename" in response.json()["detail"]


def test_unsupported_file_format_upload():
    """Test uploading unsupported format (.exe) is rejected with 400 Bad Request."""
    files = {"file": ("script.exe", b"binary content", "application/octet-stream")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


def test_empty_file_upload_rejection():
    """Test uploading an empty file is rejected with 400 Bad Request."""
    files = {"file": ("empty.txt", b"", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "file is empty" in response.json()["detail"]


def test_oversized_file_upload_rejection():
    """Test uploading file exceeding 10MB limit is rejected."""
    large_content = b"A" * (11 * 1024 * 1024)
    files = {"file": ("huge_log.txt", large_content, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "exceeds maximum allowed limit" in response.json()["detail"]


def test_vector_store_empty_similarity_search():
    """Test searching on uninitialized or empty vector store returns empty list gracefully."""
    with patch("src.ai.vector_store.get_embeddings") as mock_emb:
        manager = VectorStoreManager()
        manager.vector_store = None
        results = manager.similarity_search_with_score("any question")
        assert results == []
