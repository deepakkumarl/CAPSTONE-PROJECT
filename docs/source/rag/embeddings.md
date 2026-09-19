# Embeddings Generation

The embedding generation component is implemented in `src/ai/embeddings.py`.

## Model Specifications

- **Model Name**: `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding Dimensions**: 384 dimensions
- **Execution Device**: CPU (`model_kwargs={"device": "cpu"}`)
- **Normalization**: Normalized L2 embeddings (`encode_kwargs={"normalize_embeddings": True}`)

## Library Instantiation Strategy

The `get_embeddings()` function uses a safe import fallback mechanism:

```python
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(...)
```
