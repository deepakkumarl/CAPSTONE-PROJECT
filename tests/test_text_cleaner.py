import pytest
from src.processing.text_cleaner import clean_text

def test_clean_text_basic():
    raw = "   BMW   EV   Battery   Service   \n\n\n\r\nProcedure details...   "
    cleaned = clean_text(raw)
    assert "BMW EV Battery Service" in cleaned
    assert "\r" not in cleaned

def test_clean_text_whitespace_collapse():
    raw = "Line 1\t\twith   multiple     spaces.\n\n\n\n\nLine 2"
    cleaned = clean_text(raw)
    assert "Line 1 with multiple spaces." in cleaned
    assert "\n\n\n" not in cleaned

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""
