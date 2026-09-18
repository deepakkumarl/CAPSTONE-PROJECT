import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

@patch("src.api.routes.requests.get")
def test_enhanced_health_endpoint(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["api"] == "healthy"
    assert "vector_store" in data
    assert "embeddings" in data
    assert data["ollama"] == "connected"
    assert data["llm"] == "qwen2.5:1.5b"
    assert "documents_count" in data
    assert "chunks_count" in data
