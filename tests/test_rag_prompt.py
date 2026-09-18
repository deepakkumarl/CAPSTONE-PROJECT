import pytest
from src.ai.rag import SYSTEM_PROMPT

def test_system_prompt_constraints():
    """Verify that system prompt contains strict grounding instructions."""
    assert "You are a BMW service documentation assistant." in SYSTEM_PROMPT
    assert "Answer ONLY using the provided context." in SYSTEM_PROMPT
    assert "Do not use outside knowledge." in SYSTEM_PROMPT
    assert "say that the available documentation does not contain sufficient information." in SYSTEM_PROMPT
    assert "Do not invent procedures, specifications, diagnostic steps" in SYSTEM_PROMPT
