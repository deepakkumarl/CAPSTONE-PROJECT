# Pytest Coverage Reporting

Test coverage is configured via `pytest-cov`.

## Target Threshold
- **Coverage Goal**: $\ge 80\%$ statement coverage on application source files (`src/`).
- **Report Outputs**:
  - Terminal coverage breakdown (`--cov-report=term-missing`)
  - XML coverage report (`--cov-report=xml` saved to `coverage.xml`) used by SonarQube / SonarCloud.

## Generating Coverage Reports

```bash
pytest --cov=src --cov-report=term-missing --cov-report=xml
```
