import re

def clean_text(text: str) -> str:
    """
    Clean and normalize raw extracted document text.
    - Standardizes line breaks
    - Removes non-printable characters
    - Collapses multiple whitespace spaces while preserving paragraph breaks
    """
    if not text:
        return ""

    # Replace carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove non-printable control characters except line endings and tabs
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Normalize horizontal whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse more than 2 consecutive newlines into 2 (paragraph boundary)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
