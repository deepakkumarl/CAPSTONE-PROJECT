# Test Strategy & Test Modules

Overview of test modules in `tests/`.

| Test File | Category | Focus Area |
| :--- | :--- | :--- |
| `test_api_health.py` | API | Health check schema compliance |
| `test_enhanced_health.py` | API | Component health statuses (`components` dict) |
| `test_chunker.py` | Unit | Character splitting and `chunk_id` metadata generation |
| `test_document_deletion.py` | Unit / API | Document deletion, chunk cleanup, and FAISS rebuilding |
| `test_empty_query.py` | API | HTTP 400 Bad Request on empty questions |
| `test_evaluation.py` | Benchmark | Single test case and suite evaluation functions |
| `test_feedback.py` | API | `/feedback` endpoint and JSON persistence |
| `test_ingestion_formats.py` | Ingestion | PDF, TXT, DOCX, CSV parsing |
| `test_metadata.py` | Ingestion | Metadata attribute standardization |
| `test_query_history.py` | Utils | Query history logging and retention |
| `test_query_validation.py` | API | Request body validation |
| `test_rag_prompt.py` | AI | Grounding system prompt formatting |
| `test_resilience_and_errors.py` | Resilience | Ollama offline, path traversal, file upload limits |
| `test_retrieval_formatting.py` | Retriever | Threshold filtering and score calculation |
| `test_source_deduplication.py` | Retriever | Source deduplication by document page |
| `test_text_cleaner.py` | Processing | Whitespace normalization and line break cleaning |
