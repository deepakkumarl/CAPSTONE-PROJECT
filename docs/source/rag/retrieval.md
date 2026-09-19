# Retrieval & Relevance Thresholding

Vector retrieval logic is implemented in `ServiceKnowledgeRetriever` (`src/ai/retriever.py`).

## Retrieval Algorithm

1. **Vector Querying**: The retriever queries the FAISS index via `similarity_search_with_score(query, k=top_k)`.
2. **Score Normalization**: FAISS computes L2 distance $D \ge 0$. The score is normalized to relevance $S \in [0.0, 1.0]$:
   $$S = \max\left(0.0, \min\left(1.0, 1.0 - \frac{D}{2.0}\right)\right)$$
3. **Thresholding**: Chunks with $S < \text{similarity\_threshold}$ (default $0.35$) are discarded.
4. **Source Deduplication**:
   - Unique key: `${source}_p${page}_${chunk_id}`
   - Retains the highest-scoring chunk when multiple entries share identical document and page metadata.
5. **Output**: Returns tuple of `(relevant_documents, unique_sources_metadata_list)` sorted by similarity score in descending order.
