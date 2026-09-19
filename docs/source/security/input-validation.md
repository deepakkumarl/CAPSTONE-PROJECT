# Input Validation & Sanitization

Security safeguards enforced in `src/api/routes.py`.

## 1. Path Traversal Prevention
Uploaded filenames are extracted using `Path(filename).name`. Filenames containing path traversal tokens (`..`, `/`, `\`) or empty names return `400 Bad Request`.

## 2. File Format Restricting
Uploads are restricted to explicitly allowed extensions (`.pdf`, `.txt`, `.docx`, `.csv`).

## 3. File Size & Empty Upload Controls
- **10 MB Size Limit**: Uploads exceeding 10,485,760 bytes return `400 Bad Request`.
- **0-Byte Rejection**: Empty files return `400 Bad Request`.
