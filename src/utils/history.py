import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("query_history")

class QueryHistoryManager:
    """Manages lightweight JSON local persistence for technician diagnostic queries."""

    def __init__(self, history_file: Path = settings.HISTORY_FILE_PATH):
        self.history_file = Path(history_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_entry(
        self,
        question: str,
        answer: str,
        sources: List[Dict[str, Any]],
        status: str = "success"
    ) -> Dict[str, Any]:
        """Appends a new query execution entry to local history."""
        retrieved_docs = list(set([s.get("document", "Unknown") for s in sources]))
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "answer": answer,
            "retrieved_documents": retrieved_docs,
            "sources_count": len(sources),
            "sources": sources,
            "status": status
        }

        try:
            history = self.get_history()
            history.insert(0, entry)  # Prepend newest query first
            # Keep max 100 recent entries
            history = history[:100]

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)

            logger.info(f"Recorded query entry in history: '{question[:30]}...'")
            return entry
        except Exception as e:
            logger.error(f"Failed to record query history: {e}")
            return entry

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent query history items up to limit."""
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                return history[:limit]
        except Exception as e:
            logger.error(f"Error reading query history file: {e}")
            return []

    def clear_history(self):
        """Clears all query history records."""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f)
            logger.info("Cleared query history.")
        except Exception as e:
            logger.error(f"Failed to clear query history: {e}")


class FeedbackManager:
    """Manages lightweight JSON local persistence for user feedback (thumbs up/down)."""

    def __init__(self, feedback_file: Path = settings.FEEDBACK_FILE_PATH):
        self.feedback_file = Path(feedback_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.feedback_file.exists():
            self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.feedback_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_feedback(
        self,
        query: str,
        answer: str,
        helpful: bool,
        reason: Optional[str] = None,
        comments: Optional[str] = None
    ) -> Dict[str, Any]:
        """Appends a new user feedback record to local storage."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "answer": answer,
            "helpful": helpful,
            "reason": reason,
            "comments": comments
        }

        try:
            feedbacks = self.get_feedback()
            feedbacks.insert(0, entry)
            feedbacks = feedbacks[:200]

            with open(self.feedback_file, "w", encoding="utf-8") as f:
                json.dump(feedbacks, f, indent=2)

            logger.info(f"Recorded user feedback (helpful={helpful}) for query: '{query[:30]}...'")
            return entry
        except Exception as e:
            logger.error(f"Failed to record feedback: {e}")
            return entry

    def get_feedback(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent user feedback items."""
        if not self.feedback_file.exists():
            return []
        try:
            with open(self.feedback_file, "r", encoding="utf-8") as f:
                feedbacks = json.load(f)
                return feedbacks[:limit]
        except Exception as e:
            logger.error(f"Error reading feedback file: {e}")
            return []
