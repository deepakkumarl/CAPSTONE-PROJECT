# GitHub Actions Workflow

The main CI/CD workflow file is `.github/workflows/tests.yml`.

## Trigger Events
- `push` to `main` or `master` branch.
- `pull_request` targeting `main` or `master` branch.

## Pipeline Steps
1. **Checkout**: Uses `actions/checkout@v3` with deep fetch (`fetch-depth: 0`) for git history.
2. **Python Setup**: Uses `actions/setup-python@v4` with Python `3.11`.
3. **Dependencies**: Upgrades `pip` and installs `requirements.txt`.
4. **Flake8**: Validates code syntax and complexity (`--max-complexity=10 --max-line-length=120`).
5. **Bandit**: Runs static AST security analysis (`bandit -r src`).
6. **Pytest & Coverage**: Runs unit test suite and generates `coverage.xml`.
7. **SonarCloud**: Analyzes quality gate metrics and test coverage.
8. **Sphinx Documentation**: Executes `sphinx-build -b html docs/source docs/build/html` to verify documentation builds without errors.
9. **Docker Build**: Verifies container build (`docker build . -t bmw-service-rag:latest`).
