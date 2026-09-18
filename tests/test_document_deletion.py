import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from langchain_core.documents import Document
from src.ai.vector_store import VectorStoreManager


def test_delete_document_unit():
    """Unit test: verify delete_document correctly removes chunks from FAISS docstore."""
    with patch("src.ai.vector_store.get_embeddings") as mock_get_emb:
        mock_emb = MagicMock()
        # Embedding dimension must match (384 for MiniLM, use small for test)
        mock_emb.embed_documents.return_value = [[0.1] * 10, [0.2] * 10]
        mock_emb.embed_query.return_value = [0.1] * 10
        mock_get_emb.return_value = mock_emb

        manager = VectorStoreManager()

        doc1 = Document(
            page_content="Content EV overheating",
            metadata={
                "document_id": "sample_ev_battery_service.txt",
                "document": "sample_ev_battery_service.txt",
                "source": "sample_ev_battery_service.txt",
                "page": 1,
                "chunk_id": "c1",
                "document_type": "TXT"
            }
        )
        doc2 = Document(
            page_content="Content charging system",
            metadata={
                "document_id": "sample_charging_system.txt",
                "document": "sample_charging_system.txt",
                "source": "sample_charging_system.txt",
                "page": 1,
                "chunk_id": "c2",
                "document_type": "TXT"
            }
        )

        manager.add_documents([doc1, doc2])
        assert manager.get_total_chunks_count() == 2

        # Delete sample_ev_battery_service.txt
        success, removed_cnt, doc_name = manager.delete_document("sample_ev_battery_service.txt")
        assert success is True
        assert removed_cnt == 1
        assert doc_name == "sample_ev_battery_service.txt"
        assert manager.get_total_chunks_count() == 1

        # Delete non-existent document
        success_non, removed_non, _ = manager.delete_document("nonexistent_file.txt")
        assert success_non is False
        assert removed_non == 0

        # Remaining document info check
        info = manager.get_indexed_documents_info()
        filenames = [item["filename"] for item in info]
        assert "sample_ev_battery_service.txt" not in filenames
        assert "sample_charging_system.txt" in filenames


def test_delete_all_documents_empties_store():
    """Unit test: deleting all documents leaves the store empty."""
    with patch("src.ai.vector_store.get_embeddings") as mock_get_emb:
        mock_emb = MagicMock()
        mock_emb.embed_documents.return_value = [[0.1] * 10]
        mock_emb.embed_query.return_value = [0.1] * 10
        mock_get_emb.return_value = mock_emb

        manager = VectorStoreManager()

        doc1 = Document(
            page_content="Only document content",
            metadata={
                "document_id": "only_doc.txt",
                "document": "only_doc.txt",
                "source": "only_doc.txt",
                "page": 1,
                "chunk_id": "c_only",
                "document_type": "TXT"
            }
        )

        manager.add_documents([doc1])
        assert manager.get_total_chunks_count() == 1

        success, removed_cnt, _ = manager.delete_document("only_doc.txt")
        assert success is True
        assert removed_cnt == 1
        assert manager.get_total_chunks_count() == 0
        assert manager.vector_store is None


def test_get_indexed_documents_info_consistent_with_delete():
    """Verifies get_indexed_documents_info and delete_document use the same metadata keys."""
    with patch("src.ai.vector_store.get_embeddings") as mock_get_emb:
        mock_emb = MagicMock()
        mock_emb.embed_documents.return_value = [[0.1] * 10, [0.2] * 10, [0.3] * 10]
        mock_emb.embed_query.return_value = [0.1] * 10
        mock_get_emb.return_value = mock_emb

        manager = VectorStoreManager()

        docs = [
            Document(page_content=f"Content {i}", metadata={
                "document_id": f"doc_{i}.txt",
                "document": f"doc_{i}.txt",
                "source": f"doc_{i}.txt",
                "page": 1,
                "chunk_id": f"chunk_{i}",
                "document_type": "TXT"
            }) for i in range(3)
        ]

        manager.add_documents(docs)
        info = manager.get_indexed_documents_info()
        listed_filenames = {item["filename"] for item in info}
        assert len(listed_filenames) == 3

        # Delete doc_1.txt using the SAME identifier returned by get_indexed_documents_info
        target = "doc_1.txt"
        assert target in listed_filenames

        success, removed, _ = manager.delete_document(target)
        assert success is True
        assert removed == 1

        info_after = manager.get_indexed_documents_info()
        filenames_after = {item["filename"] for item in info_after}
        assert target not in filenames_after
        assert len(filenames_after) == 2


def test_delete_document_api_workflow_16a_16h():
    """
    Tests exact requirements 16A-16H:
    A. Ingest sample_ev_battery_service.txt
    B. Verify /documents
    C. Query 'What should be checked when an EV reports repeated battery overheating?'
    D. Confirm document is retrieved as source
    E. Delete sample_ev_battery_service.txt
    F. Verify /documents no longer lists it
    G. Query same question again
    H. Confirm deleted document is no longer returned as source
    """
    # Import app fresh — the routes module creates global instances at import time
    from src.api.main import app
    client = TestClient(app)

    # A. Ingest documents
    res_ingest = client.post("/ingest")
    assert res_ingest.status_code == 200

    # B. Verify /documents
    res_docs = client.get("/documents")
    assert res_docs.status_code == 200
    docs_list = res_docs.json()["documents"]
    filenames = [d["filename"] for d in docs_list]
    assert "sample_ev_battery_service.txt" in filenames

    # C & D. Query question & confirm retrieval
    with patch("src.ai.rag.get_llm") as mock_llm:
        mock_llm.return_value.invoke.return_value.content = "Check coolant pump V54."
        query_payload = {"question": "What should be checked when an EV reports repeated battery overheating?"}
        res_q1 = client.post("/query", json=query_payload)
        assert res_q1.status_code == 200
        sources_1 = [s["document"] for s in res_q1.json()["sources"]]
        assert "sample_ev_battery_service.txt" in sources_1

    # E. Delete sample_ev_battery_service.txt
    res_del = client.delete("/documents/sample_ev_battery_service.txt")
    assert res_del.status_code == 200
    del_data = res_del.json()
    assert del_data["status"] == "success"
    assert del_data["document"] == "sample_ev_battery_service.txt"
    assert del_data["chunks_removed"] > 0

    # F. Verify /documents no longer lists it
    res_docs_2 = client.get("/documents")
    assert res_docs_2.status_code == 200
    filenames_2 = [d["filename"] for d in res_docs_2.json()["documents"]]
    assert "sample_ev_battery_service.txt" not in filenames_2

    # Attempt to delete non-existent document -> 404
    res_del_404 = client.delete("/documents/nonexistent_doc.txt")
    assert res_del_404.status_code == 404

    # G & H. Query same question again & confirm deleted document is NOT returned
    with patch("src.ai.rag.get_llm") as mock_llm2:
        mock_llm2.return_value.invoke.return_value.content = "I could not find sufficient information in the available BMW service documentation."
        res_q2 = client.post("/query", json=query_payload)
        assert res_q2.status_code == 200
        sources_2 = [s["document"] for s in res_q2.json()["sources"]]
        assert "sample_ev_battery_service.txt" not in sources_2
