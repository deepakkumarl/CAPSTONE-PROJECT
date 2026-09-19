# User Acceptance Testing (UAT) Protocol

This document defines the formal User Acceptance Testing (UAT) scenarios, step-by-step procedures, expected behavior, and verification criteria for the BMW Service Knowledge RAG platform.

---

## Scenario 1: Happy Path — Ingestion, Querying & Citation

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 1.1 | Upload `sample_ev_battery_service.txt` via UI or `POST /upload` | API returns HTTP 200 with status `"success"` and chunk count $\ge 1$. | PASSED |
| 1.2 | Check Knowledge Base Dashboard / `GET /documents` | `sample_ev_battery_service.txt` appears listed with chunk statistics. | PASSED |
| 1.3 | Submit query: *"What should be checked when an EV reports repeated battery overheating?"* | API returns HTTP 200 with grounded answer citing `sample_ev_battery_service.txt`. | PASSED |
| 1.4 | Inspect response UI | Grounding badge displays `HIGH` 🟢 with source document name and relevance score. | PASSED |

---

## Scenario 2: Invalid Input Handling

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 2.1 | Submit query with empty string `""` | API returns HTTP 400 Bad Request: `"Question field cannot be empty."` | PASSED |
| 2.2 | Upload unsupported `.exe` or `.bin` file | API returns HTTP 400 Bad Request: `"Unsupported file format"`. | PASSED |
| 2.3 | Upload file with path traversal filename `../../passwd.txt` | API returns HTTP 400 Bad Request: `"Invalid or malicious filename"`. | PASSED |

---

## Scenario 3: Out-of-Domain / Missing Data Fallback

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 3.1 | Submit query not present in documentation: *"How do I reset oil change light on 1995 E36?"* | System triggers anti-hallucination fallback. | PASSED |
| 3.2 | Check response content & grounding | Output states: *"I could not find sufficient information in the available BMW service documentation."* Grounding badge displays `INSUFFICIENT` 🔴. | PASSED |

---

## Scenario 4: Duplicate Ingestion Handling

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 4.1 | Ingest `sample_ev_battery_service.txt` a second time | Ingestion pipeline checks `chunk_id` metadata. | PASSED |
| 4.2 | Verify total chunk count in `/health` | Duplicate chunks are skipped; chunk count does not duplicate uncontrollably. | PASSED |

---

## Scenario 5: Dependency Failure & Recovery

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 5.1 | Stop Ollama server (`ollama stop` or disconnect port 11434) | Ollama component reports `disconnected` 🔴 in `/health` and UI sidebar. | PASSED |
| 5.2 | Submit query while Ollama is offline | Backend API does NOT crash. Returns clean response: *"Error communicating with local LLM (Ollama)..."* | PASSED |
| 5.3 | Restart Ollama server | `/health` restores Ollama status to `connected` 🟢. Queries succeed cleanly. | PASSED |

---

## Scenario 6: Document Deletion & FAISS Persistence Verification

| Step | Action | Expected Result | Pass/Fail |
|---|---|---|---|
| 6.1 | Delete document `sample_ev_battery_service.txt` via `DELETE /documents/sample_ev_battery_service.txt` | API returns HTTP 200 with status `"success"`. | PASSED |
| 6.2 | Check `/documents` list | Document `sample_ev_battery_service.txt` is no longer listed. | PASSED |
| 6.3 | Query question again | Retrieval no longer returns `sample_ev_battery_service.txt` as source. | PASSED |
| 6.4 | Restart FastAPI backend service | FAISS index reloads from disk; deleted document remains permanently deleted. | PASSED |
