# SonarCloud Integration

SonarCloud static analysis configuration is stored in `sonar-project.properties`.

## `sonar-project.properties`

```ini
sonar.projectKey=bmw-service-knowledge-rag
sonar.projectName=BMW Service Knowledge RAG Capstone
sonar.projectVersion=1.0.0
sonar.sources=src
sonar.tests=tests
sonar.language=py
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
sonar.exclusions=data/**, .venv/**, docs/**, sql/**, terraform/**, **/__pycache__/**, *.json
```

## GitHub Secrets Configuration
- `SONAR_TOKEN`: ${{ secrets.SONAR_TOKEN }}
- `GITHUB_TOKEN`: ${{ secrets.GITHUB_TOKEN }}
