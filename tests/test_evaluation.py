import pytest
from unittest.mock import MagicMock, patch
from src.ai.evaluation import evaluate_single_test_case, run_rag_evaluation, BENCHMARK_DATASET

def test_evaluate_single_test_case_success():
    mock_rag = MagicMock()
    mock_rag.answer_question.return_value = {
        "question": "What should be checked when an EV reports repeated battery overheating?",
        "answer": "Check coolant pump V54 and DTC 21A004.",
        "sources": [{"document": "sample_ev_battery_service.txt", "page": 1, "score": 0.88}]
    }

    test_case = {
        "id": "TC-001",
        "question": "What should be checked when an EV reports repeated battery overheating?",
        "expected_document": "sample_ev_battery_service.txt",
        "expect_fallback": False
    }

    result = evaluate_single_test_case(test_case, rag_pipeline=mock_rag)

    assert result["id"] == "TC-001"
    assert result["status"] == "PASSED"
    assert result["passed"] is True
    assert result["retrieval_success"] is True
    assert result["number_of_sources"] == 1
    assert result["error"] is None
    assert "sample_ev_battery_service.txt" in result["retrieved_documents"]

def test_evaluate_single_test_case_timeout_handling():
    mock_rag = MagicMock()
    mock_rag.answer_question.side_effect = TimeoutError("Request timed out after 35s")

    test_case = {
        "id": "TC-002",
        "question": "What are the recommended checks for a charging system fault?",
        "expected_document": "sample_charging_system.txt",
        "expect_fallback": False
    }

    result = evaluate_single_test_case(test_case, rag_pipeline=mock_rag)

    assert result["id"] == "TC-002"
    assert result["status"] == "TIMEOUT"
    assert result["passed"] is False
    assert result["retrieval_success"] is False
    assert result["number_of_sources"] == 0
    assert "TIMEOUT" in result["answer_generated"]
    assert result["error"] == "Request timed out after 35s"

def test_run_rag_evaluation_continuation_after_timeout():
    mock_rag = MagicMock()

    def mock_answer(q):
        if "charging" in q:
            raise TimeoutError("LLM response timeout")
        if "oil change" in q:
            return {
                "question": q,
                "answer": "I could not find sufficient information in the available BMW service documentation.",
                "sources": []
            }
        return {
            "question": q,
            "answer": "Grounded answer.",
            "sources": [{"document": "sample_ev_battery_service.txt", "page": 1, "score": 0.9}]
        }

    mock_rag.answer_question.side_effect = mock_answer

    report = run_rag_evaluation(rag_pipeline=mock_rag)

    assert "summary" in report
    summary = report["summary"]
    assert summary["total_test_cases"] == len(BENCHMARK_DATASET)
    assert summary["timeout_test_cases"] == 1
    assert summary["passed_test_cases"] >= 1

    # Ensure evaluation continued after TC-002 timed out
    details = report["details"]
    tc2 = next(item for item in details if item["id"] == "TC-002")
    assert tc2["status"] == "TIMEOUT"

    tc4 = next(item for item in details if item["id"] == "TC-004")
    assert tc4["status"] == "PASSED"

def test_evaluation_api_endpoints():
    from fastapi.testclient import TestClient
    from src.api.main import app

    client = TestClient(app)

    # Test GET /evaluate/dataset
    res_ds = client.get("/evaluate/dataset")
    assert res_ds.status_code == 200
    assert len(res_ds.json()["dataset"]) > 0

    # Test POST /evaluate/test-case with mock
    with patch("src.api.routes.rag_pipeline.answer_question") as mock_ans:
        mock_ans.return_value = {
            "question": "What should be checked when an EV reports repeated battery overheating?",
            "answer": "Check coolant pump V54.",
            "sources": [{"document": "sample_ev_battery_service.txt", "page": 1, "score": 0.88}]
        }
        payload = {
            "id": "TC-001",
            "question": "What should be checked when an EV reports repeated battery overheating?",
            "expected_document": "sample_ev_battery_service.txt",
            "expect_fallback": False
        }
        res_tc = client.post("/evaluate/test-case", json=payload)
        assert res_tc.status_code == 200
        data = res_tc.json()
        assert data["id"] == "TC-001"
        assert data["status"] == "PASSED"
