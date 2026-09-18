# Data Dictionary

This document details the data structures, schemas, and metadata attributes maintained across the BMW Service Knowledge RAG platform.

---

## 1. Document Schema

| Attribute Field | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `filename` | String | Original filename | `sample_ev_battery_service.txt` |
| `document_type` | String | File extension format | `PDF`, `TXT`, `DOCX`, `CSV` |
| `total_chunks` | Integer | Total vector chunks generated | `4` |
| `pages_count` | Integer | Total pages or sections | `1` |
| `status` | String | Ingestion status | `Indexed` |

---

## 2. Chunk Schema

| Attribute Field | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `chunk_id` | String | Unique identifier | `sample_ev_battery_service.txt_p1_c0_a1b2c3` |
| `source` | String | Source filename | `sample_ev_battery_service.txt` |
| `page` | Integer | Page number (1-indexed) | `1` |
| `document_type` | String | Format extension | `TXT` |
| `page_content` | String | Cleaned text (~800 chars) | `"Check high-voltage battery cooling..."` |
| `embedding` | Vector Float[384] | MiniLM-L6-v2 vector | `[0.012, -0.045, ...]` |

---

## 3. Query History Schema

| Attribute Field | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `timestamp` | String (ISO 8601) | Query execution timestamp | `2025-09-18T10:00:00Z` |
| `question` | String | Technician question | `"What should be checked when an EV reports overheating?"` |
| `answer` | String | Grounded answer | `"Check coolant pump V54..."` |
| `retrieved_documents` | List[String] | List of retrieved filenames | `["sample_ev_battery_service.txt"]` |
| `sources_count` | Integer | Deduplicated source count | `1` |
| `status` | String | Execution status | `success`, `fallback`, `error` |

---

## 4. Evaluation Benchmark Report Schema

| Attribute Field | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `total_test_cases` | Integer | Number of benchmark tests | `6` |
| `passed_test_cases` | Integer | Passed benchmark tests | `6` |
| `accuracy_percentage` | Float | Overall accuracy percentage | `100.0` |
| `status` | String | Benchmark suite status | `PASSED`, `NEEDS_ATTENTION` |
