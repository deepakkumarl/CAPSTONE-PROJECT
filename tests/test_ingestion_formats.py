import pytest
import tempfile
from pathlib import Path
from src.ingestion.document_loader import load_single_document

def test_load_txt_document():
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w+", delete=False) as tf:
        tf.write("BMW EV Battery Cooling System diagnostic steps...")
        tf_path = Path(tf.name)

    try:
        docs = load_single_document(tf_path)
        assert len(docs) == 1
        assert "Cooling System" in docs[0].page_content
        assert docs[0].metadata["document_type"] == "TXT"
    finally:
        tf_path.unlink()

def test_load_csv_document():
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=False) as tf:
        tf.write("FaultCode,Description,Component\n21A004,Battery Overheating,TMCU\n")
        tf_path = Path(tf.name)

    try:
        docs = load_single_document(tf_path)
        assert len(docs) == 1
        assert "21A004" in docs[0].page_content
        assert docs[0].metadata["document_type"] == "CSV"
    finally:
        tf_path.unlink()
