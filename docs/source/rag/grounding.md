# Grounding & Anti-Hallucination Controls

Grounding safeguards ensure that LLM answers rely exclusively on retrieved BMW service documentation context.

## Grounding Rating Metric

Grounding levels are evaluated dynamically in `RAGPipeline`:

- **`HIGH`**: Top retrieved chunk relevance score $S \ge 0.60$.
- **`MEDIUM`**: Top retrieved chunk relevance score $S \in [0.35, 0.60)$.
- **`INSUFFICIENT`**: No document chunks passed the similarity threshold ($0.35$) or retrieval returned empty results.

## Anti-Hallucination Fallback

When grounding level is `INSUFFICIENT`, the LLM invocation is skipped entirely, and the pipeline immediately outputs:

> *"I could not find sufficient information in the available BMW service documentation."*

This prevents model hallucinations on out-of-domain queries.
