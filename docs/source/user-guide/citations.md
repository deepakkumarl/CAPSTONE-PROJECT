# Source Citations & Metadata Display

To ensure complete diagnostic transparency and auditability, all generated answers display unique source citations.

## Citation Card Structure

Under each assistant response, supporting sources are rendered inside expandable cards:

```
Source 1: sample_ev_battery_service.txt — Page 1 [Relevance: 0.82]
-------------------------------------------------------------------
Document: sample_ev_battery_service.txt
Type: TXT
Page: 1
Relevance: 0.82
```

### Fields Displayed
- **Document Name**: Clean filename basename (e.g., `sample_ev_battery_service.txt`).
- **Document Type**: Extracted file format (`PDF`, `TXT`, `DOCX`, `CSV`).
- **Page Number**: 1-indexed page or document section number.
- **Relevance Score**: Normalized score $S \in [0.0, 1.0]$ where $1.0$ represents exact semantic match.
- **Debug Metadata**: Optional toggle displaying internal `chunk_id` and text snippet preview.

## Source Deduplication Rules

The `ServiceKnowledgeRetriever` deduplicates candidate search results before constructing prompt context:
- Deduplication key: `${document}_p${page}_${chunk_id}`
- When multiple chunks originate from the same page, the retriever preserves the chunk with the highest similarity score.
- Prevents redundant source listings for the same document page.
