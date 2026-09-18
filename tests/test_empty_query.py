import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_empty_string_query():
    payload = {"question": "   "}
    response = client.post("/query", json=payload)
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_missing_question_field():
    payload = {}
    response = client.post("/query", json=payload)
    assert response.status_code == 422  # Pydantic validation error
