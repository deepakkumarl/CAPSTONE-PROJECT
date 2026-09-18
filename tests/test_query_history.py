import pytest
import tempfile
from pathlib import Path
from src.utils.history import QueryHistoryManager

def test_query_history_manager():
    with tempfile.TemporaryDirectory() as tmp_dir:
        hist_file = Path(tmp_dir) / "query_history.json"
        manager = QueryHistoryManager(history_file=hist_file)

        assert manager.get_history() == []

        sources = [{"document": "sample_ev_battery_service.txt", "page": 1, "score": 0.88}]
        manager.add_entry(
            question="What should be checked when an EV reports overheating?",
            answer="Check coolant pump V54.",
            sources=sources,
            status="success"
        )

        history = manager.get_history()
        assert len(history) == 1
        assert history[0]["question"] == "What should be checked when an EV reports overheating?"
        assert history[0]["sources_count"] == 1
        assert "sample_ev_battery_service.txt" in history[0]["retrieved_documents"]
