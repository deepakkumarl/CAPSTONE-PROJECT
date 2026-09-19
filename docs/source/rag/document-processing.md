# Document Processing & Text Cleaning

Document loading and text cleaning modules are implemented in `src/ingestion/document_loader.py` and `src/processing/text_cleaner.py`.

## 1. Multi-Format Text Extraction

- **PDF Files (`.pdf`)**: Extracted page by page using `pypdf.PdfReader`. Text content per page is processed independently with page-level metadata assignment (`page=1, 2, ...`).
- **Text Files (`.txt`)**: Read with UTF-8 encoding (fallback `errors="ignore"`).
- **Word Documents (`.docx`)**: Parsed paragraph by paragraph using `python-docx`. Non-empty paragraphs are joined with line breaks.
- **CSV Files (`.csv`)**: Parsed row by row using Python standard `csv.reader`. Rows are converted into comma-separated text representations.

## 2. Text Normalization (`clean_text`)

The `clean_text` function in `src/processing/text_cleaner.py` performs the following operations:
1. **Line Break Normalization**: Converts `\r\n` and `\r` to `\n`.
2. **Control Character Stripping**: Removes non-printable characters matching regex `[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]`.
3. **Horizontal Whitespace Collapsing**: Collapses multiple consecutive spaces and tabs into a single space (`[ \t]+` -> `" "`).
4. **Paragraph Boundary Preservation**: Limits consecutive line breaks to a maximum of 2 (`\n{3,}` -> `\n\n`).
