# Product Requirement Document (PRD)

## Project Name: BMW Service Knowledge RAG

### 1. Product Overview
The **BMW Service Knowledge RAG** platform is an enterprise-grade AI technical assistant for BMW service technicians. It enables mechanics to search service documentation (PDF, TXT, DOCX, CSV) and receive grounded diagnostic answers with unique source citations, dynamic similarity controls, local query history, and an automated benchmark evaluation suite.

### 2. Key Enhancements & Upgrades
- **Multi-Tab Streamlit UI**: Chat interface, Knowledge Base Dashboard, Query History log, and RAG Evaluation Benchmark.
- **Source Deduplication**: Deduplicates source citations by `(document, page)` and `chunk_id`.
- **Document Management & Index Rebuilding**: Document deletion removes target vectors and safely rebuilds the FAISS index.
- **Automated RAG Evaluation**: Built-in benchmark evaluator testing retrieval precision and anti-hallucination fallback.
- **Enhanced Health Monitoring**: Active status monitoring for FastAPI, FAISS, Embeddings, and Ollama connectivity (`http://localhost:11434/api/tags`).

### 3. Acceptance Criteria
- **AC-1 Grounding**: Assistant must retrieve relevant documents before answering. If insufficient, output:
  > *"I could not find sufficient information in the available BMW service documentation."*
- **AC-2 Unique Citations**: Sources are deduplicated; no duplicate source entries for the same document page.
- **AC-3 Local Privacy**: 100% local execution using Ollama `qwen2.5:1.5b` and local sentence transformers (`all-MiniLM-L6-v2`).
