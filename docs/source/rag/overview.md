# RAG System Overview

The BMW Service Knowledge RAG platform uses a local, multi-stage RAG architecture to provide high-precision technical answers from service manuals.

## Core RAG Parameters

| Parameter | Value | Configuration Source |
| :--- | :--- | :--- |
| **Chunk Size** | `800` characters | `src/utils/config.py` (`CHUNK_SIZE`) |
| **Chunk Overlap** | `100` characters | `src/utils/config.py` (`CHUNK_OVERLAP`) |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` | `src/utils/config.py` (`EMBEDDING_MODEL`) |
| **Top K Chunks** | `5` chunks | `src/utils/config.py` (`TOP_K`) |
| **Similarity Threshold** | `0.35` (Normalized $[0.0, 1.0]$) | `src/utils/config.py` (`SIMILARITY_THRESHOLD`) |
| **Local LLM Model** | `qwen2.5:1.5b` | `src/utils/config.py` (`OLLAMA_MODEL`) |
| **LLM Temperature** | `0.0` (Deterministic) | `src/ai/llm.py` |
