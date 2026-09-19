# Contributing & Quality Standards

Guidelines for submitting code contributions to the repository.

## Contribution Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Implement your changes keeping code modular and clean.
3. Run linting: `flake8 src`
4. Run security analysis: `bandit -r src`
5. Run Pytest suite & verify coverage:
   ```bash
   pytest --verbose --cov=src --cov-report=term-missing --cov-report=xml
   ```
6. Build Sphinx documentation:
   ```bash
   sphinx-build -b html docs/source docs/build/html
   ```
7. Open a Pull Request targeting `main`.
