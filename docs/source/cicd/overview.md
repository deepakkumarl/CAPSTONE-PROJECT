# CI/CD Pipeline Overview

The CI/CD pipeline automates testing, code quality checks, security auditing, documentation builds, and container image generation.

```
Git Push / Pull Request to main
           │
           v
GitHub Actions Runner (.github/workflows/tests.yml)
           │
           ├── 1. Setup Python 3.11
           ├── 2. Install Dependencies
           ├── 3. Flake8 Linting
           ├── 4. Bandit Security Scan
           ├── 5. Pytest & Coverage (coverage.xml)
           ├── 6. SonarCloud Code Analysis
           ├── 7. Sphinx Documentation Build (sphinx-build -b html)
           └── 8. Docker Build & Push (deepakkumar889/bmw-service-rag:latest)
```
