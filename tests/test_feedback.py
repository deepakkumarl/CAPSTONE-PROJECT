import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.utils.history import FeedbackManager

client = TestClient(app)


def test_submit_feedback_endpoint():
    """Test submitting feedback via POST /feedback endpoint."""
    payload = {
        "query": "What should be checked when an EV reports repeated battery overheating?",
        "answer": "Check coolant flow and temp sensors.",
        "helpful": True,
        "reason": "Accurate details",
        "comments": "Very clear instructions."
    }
    response = client.post("/feedback", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Feedback recorded successfully."


def test_feedback_manager_persistence(tmp_path):
    """Test FeedbackManager stores feedback in JSON file correctly."""
    fb_file = tmp_path / "test_feedback.json"
    manager = FeedbackManager(feedback_file=fb_file)

    entry = manager.add_feedback(
        query="Charging issue?",
        answer="Inspect CP/PP signals.",
        helpful=False,
        reason="Missing torque values",
        comments="Please add torque specs."
    )

    assert entry["query"] == "Charging issue?"
    assert entry["helpful"] is False

    records = manager.get_feedback()
    assert len(records) == 1
    assert records[0]["reason"] == "Missing torque values"
