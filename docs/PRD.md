# Product Requirement Document (PRD)

## Project Name: BMW Service Knowledge RAG

### 1. Product Overview
The **BMW Service Knowledge RAG** system is an AI-powered technical assistance application designed for BMW service technicians. It provides accurate, grounded answers to complex diagnostic questions by retrieving relevant service documentation and leveraging a local, privacy-compliant Large Language Model (Ollama with `qwen2.5:1.5b`).

### 2. Problem Statement
BMW service technicians must navigate extensive technical documentation, service manuals, and diagnostic bulletins during vehicle troubleshooting. Finding specific diagnostic steps, sensor checks, or fault codes under time constraints can delay repairs. Technicians need an immediate, natural-language search assistant that guarantees answers are grounded exclusively in official service manuals without introducing unverified assumptions or hallucinations.

### 3. Target Users
- Primary: BMW Service Technicians & Master Mechanics
- Secondary: Technical Workshop Managers & Service Advisors

### 4. Goals
- Fast, natural language query resolution for vehicle service procedures.
- Grounded answers strictly based on uploaded service documentation (PDF, TXT, DOCX).
- Transparent source citation (document name, page numbers, similarity scores).
- Local processing with 0 data egress (Ollama local LLM execution).

### 5. Non-Goals
- Executing live vehicle telemetry or OBD-II active CAN bus control.
- Commercial billing, repair order management, or inventory tracking.
- Replacing certified technician safety protocols or official ISTA diagnostic hardware.

### 6. Functional Requirements
- **FR-1 Document Upload & Ingestion**: The system must ingest PDF, TXT, and DOCX documentation, extract text, clean formatting, split into ~800 character chunks with 100 character overlap, and store embeddings in FAISS.
- **FR-2 Grounded RAG Search**: For any technician question, the assistant must retrieve top-K relevant chunks from FAISS vector store before attempting answer generation.
- **FR-3 Strict Grounding & Anti-Hallucination**: The system prompt must instruct the local LLM to answer strictly from the retrieved context. If relevant documentation is absent, the system must return:
  > *"I could not find sufficient information in the available BMW service documentation."*
- **FR-4 Source Citation**: Every generated response must list supporting document filenames and page numbers.

### 7. Non-Functional Requirements
- **NFR-1 Latency**: Query retrieval and response generation under 15 seconds on a standard developer laptop.
- **NFR-2 Security**: 100% local execution using Ollama `qwen2.5:1.5b` and local SentenceTransformers embeddings without external API calls.
- **NFR-3 Reliability**: Fallback handling for missing documents, offline Ollama instance, or low-confidence queries.

### 8. User Stories
1. *As a technician*, I want to ask *"What should be checked when an EV reports repeated battery overheating?"* so that I receive immediate, step-by-step diagnostic checks.
2. *As a workshop lead*, I want to upload new service PDF bulletins via the UI so that the team can search newly released technical documentation.

### 9. RAG Workflow
```
[Document Upload / Sample Data]
            │
            ▼
   [PyPDF / Text Loader]
            │
            ▼
    [Clean & Chunker]
            │
            ▼
[SentenceTransformers Embedding]
            │
            ▼
     [FAISS Indexing]
            │
    [Technician Question]
            │
            ▼
    [FAISS Top-K Search]
            │
            ▼
 [Relevance Threshold Filter]
      │              │
    (Pass)         (Fail) ──► ["I could not find sufficient information..."]
      │
      ▼
[Strict Grounding Prompt]
      │
      ▼
 [Ollama qwen2.5:1.5b]
      │
      ▼
[Streamlit UI + Citations]
```

### 10. Acceptance Criteria
- **AC-1 Pre-Retrieval Requirement**: The assistant MUST retrieve relevant documentation BEFORE generating the final answer.
- **AC-2 No General LLM Hallucinations**: Answers must be strictly derived from retrieved text; if threshold criteria are not met, return the standardized insufficient information message.
- **AC-3 Complete Source Attribution**: Source filenames and page numbers must accompany every valid answer.
