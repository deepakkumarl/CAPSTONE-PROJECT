import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

@patch("src.api.routes.rag_pipeline.answer_question")
def test_query_validation_success(mock_answer):
    mock_answer.return_value = {
        "question": "What should be checked when an EV reports repeated battery overheating?",
        "answer": "Check coolant pump V54 and DTC 21A004.",
        "sources": [
            {
                "document": "sample_ev_battery_service.txt",
                "page": 1,
                "document_type": "TXT",
                "score": 0.88,
                "chunk_id": "chunk_123"
            }
        ]
    }

    payload = {"question": "What should be checked when an EV reports repeated battery overheating?"}
    response = client.post("/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == payload["question"]
    assert "coolant pump V54" in data["answer"]
    assert len(data["sources"]) == 1
    assert data["sources"][0]["document"] == "sample_ev_battery_service.txt"
