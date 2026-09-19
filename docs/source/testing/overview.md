# Testing Overview

The platform uses **Pytest** for automated unit and integration testing.

## Automated Test Command

```bash
pytest --verbose --cov=src --cov-report=term-missing --cov-report=xml
```

- **Total Test Cases**: 34 tests across 17 test modules.
- **Pass Rate**: 100% (34 passed, 0 failed).
- **Test Execution Mode**: Fully mocked external LLM / network dependencies (`unittest.mock.patch`). Runs deterministically without requiring a live Ollama server.
