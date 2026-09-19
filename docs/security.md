# Security Architecture & Code Quality Guidelines

This document details security controls, static application security testing (SAST), path traversal safeguards, and data privacy policies.

---

## 1. Security Safeguards & Controls

### Path Traversal Prevention
Uploaded filenames are passed through `Path(filename).name` sanitization. Filenames containing `..`, slashes (`/`, `\`), or empty strings are immediately rejected with `400 Bad Request`.

### Upload File Validation & File Size Control
- **Allowed Formats**: `.pdf`, `.txt`, `.docx`, `.csv`
- **Max File Size**: 10 MB limit per file upload.
- **Empty Files**: 0-byte uploads are rejected.

### Local Privacy
All query processing, embeddings generation, vector storage, and LLM text generation occur 100% locally. No document text or technician query data is transmitted to external cloud APIs.

---

## 2. Security Scanning & AST Tools

### Bandit (Python AST Security Scanner)
Runs static code analysis for common security flaws (hardcoded passwords, unsafe deserialization, etc.):
```bash
bandit -r src
```

### Flake8 (Code Quality & Style Checks)
```bash
flake8 src --max-line-length=120
```

### SonarQube / SonarCloud Integration
Static analysis configuration is maintained in `sonar-project.properties` and integrated into `.github/workflows/tests.yml`.
