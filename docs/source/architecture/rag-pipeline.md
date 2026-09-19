# RAG Pipeline Architecture

The end-to-end Retrieval-Augmented Generation (RAG) pipeline is orchestrated by `RAGPipeline` in `src/ai/rag.py`.

```
User Question
      │
      v
+------------------------------------+
| ServiceKnowledgeRetriever          |
| - Similarity Search (top_k=5)      |
| - Threshold Filtering (>= 0.35)    |
| - Source Deduplication             |
+------------------------------------+
      │
      ├──────────────────────────────┐
      │ (If no docs pass threshold)  │ (If docs pass threshold)
      v                              v
+------------------------+  +------------------------------------+
| Grounded Fallback      |  | Prompt Template Formatting         |
| Response Output        |  | - Insert context chunks           |
| (Grounding:            |  | - Strict system prompt directives  |
|  INSUFFICIENT)         |  +------------------------------------+
+------------------------+                    │
                                              v
                                    +------------------------------------+
                                    | Ollama Local LLM (qwen2.5:1.5b)    |
                                    | - Generate grounded answer         |
                                    +------------------------------------+
                                              │
                                              v
                                    +------------------------------------+
                                    | Response & Source Citations        |
                                    | (Grounding: HIGH / MEDIUM)         |
                                    +------------------------------------+
```

## Step-by-Step Execution Sequence

1. **Input Validation**: The pipeline validates that the incoming diagnostic query is non-empty.
2. **Dense Vector Search**: The `ServiceKnowledgeRetriever` (`src/ai/retriever.py`) converts the query into a 384-dimensional vector using `all-MiniLM-L6-v2` and retrieves top $K$ ($K=5$) nearest neighbors from the FAISS index.
3. **Similarity Score Normalization**: Raw FAISS L2 Euclidean distances ($D$) are converted to a normalized relevance score $S \in [0.0, 1.0]$:
   $$S = \max\left(0.0, \min\left(1.0, 1.0 - \frac{D}{2.0}\right)\right)$$
4. **Threshold Validation**: Chunks with $S < 0.35$ are filtered out. If zero chunks pass the threshold, the pipeline returns the anti-hallucination fallback response:
   > *"I could not find sufficient information in the available BMW service documentation."*
5. **Source Deduplication**: Retrieved chunks are deduplicated by `(document, page)` and `chunk_id`, preserving the highest similarity score.
6. **Prompt Assembly & LLM Generation**: Qualified context chunks are formatted into the system prompt and sent to Ollama `qwen2.5:1.5b` with zero temperature (`temperature=0.0`).
7. **Grounding Level Assignment**:
   - `HIGH`: Top source score $\ge 0.60$
   - `MEDIUM`: Top source score $\in [0.35, 0.60)$
   - `INSUFFICIENT`: Fallback triggered or score $< 0.35$
