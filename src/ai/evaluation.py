from typing import Dict, Any, List, Optional
from src.ai.rag import RAGPipeline, FALLBACK_RESPONSE
from src.utils.logging_config import setup_logger

logger = setup_logger("evaluation")

BENCHMARK_DATASET = [
    {
        "id": "TC-001",
        "question": "What should be checked when an EV reports repeated battery overheating?",
        "expected_document": "sample_ev_battery_service.txt",
        "expect_fallback": False
    },
    {
        "id": "TC-002",
        "question": "What are the recommended checks for a charging system fault?",
        "expected_document": "sample_charging_system.txt",
        "expect_fallback": False
    },
    {
        "id": "TC-003",
        "question": "What checks should be performed on the battery cooling circuit?",
        "expected_document": "sample_thermal_management.txt",
        "expect_fallback": False
    },
    {
        "id": "TC-004",
        "question": "How do I reset the oil change service light on a 1995 E36 3-Series?",
        "expected_document": None,
        "expect_fallback": True
    },
    {
        "id": "TC-005",
        "question": "What is the recommended brake fluid change interval for a bicycle?",
        "expected_document": None,
        "expect_fallback": True
    }
]


def evaluate_single_test_case(
    test_case: Dict[str, Any],
    rag_pipeline: Optional[RAGPipeline] = None
) -> Dict[str, Any]:
    """
    Evaluates a single benchmark test case through the production RAG pipeline.
    Handles individual test case timeouts and errors gracefully.
    """
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()

    tc_id = test_case.get("id", "TC-UNK")
    question = test_case.get("question", "")
    expected_doc = test_case.get("expected_document")
    expect_fallback = test_case.get("expect_fallback", False)

    logger.info(f"Evaluating benchmark test case {tc_id}: '{question[:30]}...'")

    try:
        result = rag_pipeline.answer_question(question)
        answer = result.get("answer", "")
        sources = result.get("sources", [])

        retrieved_docs = list(set([s.get("document", "") for s in sources]))
        is_fallback = (answer == FALLBACK_RESPONSE or FALLBACK_RESPONSE in answer)

        # Evaluate Retrieval Success
        if expect_fallback:
            retrieval_success = (len(sources) == 0)
            test_passed = is_fallback and retrieval_success
            note = "Correctly triggered anti-hallucination fallback" if test_passed else "Failed to trigger fallback on out-of-domain query"
        else:
            doc_matched = any(expected_doc in d for d in retrieved_docs) if expected_doc else True
            retrieval_success = doc_matched and (len(sources) > 0)
            test_passed = (not is_fallback) and retrieval_success
            note = f"Retrieved expected source '{expected_doc}' and generated grounded answer" if test_passed else f"Failed to retrieve '{expected_doc}' or returned fallback"

        status_str = "PASSED" if test_passed else "FAILED"

        return {
            "id": tc_id,
            "question": question,
            "expected_document": expected_doc or "N/A (Out of Domain)",
            "retrieved_documents": retrieved_docs,
            "retrieval_success": retrieval_success,
            "number_of_sources": len(sources),
            "answer_generated": answer[:250] + "..." if len(answer) > 250 else answer,
            "fallback_expected": expect_fallback,
            "fallback_returned": is_fallback,
            "status": status_str,
            "passed": test_passed,
            "error": None,
            "evaluation_note": note
        }

    except TimeoutError as te:
        logger.warning(f"Test case {tc_id} timed out: {te}")
        return {
            "id": tc_id,
            "question": question,
            "expected_document": expected_doc or "N/A (Out of Domain)",
            "retrieved_documents": [],
            "retrieval_success": False,
            "number_of_sources": 0,
            "answer_generated": f"TIMEOUT: Evaluation request timed out for test {tc_id}.",
            "fallback_expected": expect_fallback,
            "fallback_returned": False,
            "status": "TIMEOUT",
            "passed": False,
            "error": str(te) or "Request timed out",
            "evaluation_note": f"Test case timed out during LLM response generation."
        }

    except Exception as e:
        logger.error(f"Test case {tc_id} encountered error: {e}")
        return {
            "id": tc_id,
            "question": question,
            "expected_document": expected_doc or "N/A (Out of Domain)",
            "retrieved_documents": [],
            "retrieval_success": False,
            "number_of_sources": 0,
            "answer_generated": f"ERROR: {str(e)}",
            "fallback_expected": expect_fallback,
            "fallback_returned": False,
            "status": "ERROR",
            "passed": False,
            "error": str(e),
            "evaluation_note": f"Execution error: {str(e)}"
        }


def run_rag_evaluation(rag_pipeline: Optional[RAGPipeline] = None) -> Dict[str, Any]:
    """
    Executes the entire benchmark evaluation test suite item-by-item.
    Guarantees that individual test timeouts/failures do NOT terminate the evaluation run.
    """
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()

    test_results = []
    passed_tests = 0
    timeout_tests = 0
    failed_tests = 0

    for test_case in BENCHMARK_DATASET:
        res = evaluate_single_test_case(test_case, rag_pipeline=rag_pipeline)
        test_results.append(res)

        if res["status"] == "PASSED":
            passed_tests += 1
        elif res["status"] == "TIMEOUT":
            timeout_tests += 1
        else:
            failed_tests += 1

    total_tests = len(BENCHMARK_DATASET)
    accuracy_pct = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0.0

    report = {
        "summary": {
            "total_test_cases": total_tests,
            "passed_test_cases": passed_tests,
            "failed_test_cases": failed_tests,
            "timeout_test_cases": timeout_tests,
            "accuracy_percentage": accuracy_pct,
            "status": "PASSED" if accuracy_pct >= 80.0 else "NEEDS_ATTENTION"
        },
        "details": test_results
    }

    logger.info(f"RAG Evaluation completed: {passed_tests}/{total_tests} passed, {timeout_tests} timed out ({accuracy_pct}%).")
    return report
