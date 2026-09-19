# Project Structure & Architecture

```
bmw-capstone-usecase/
├── .github/workflows/tests.yml   # CI/CD pipeline
├── data/                         # Data storage (sample, uploads, vectorstore, history, feedback)
├── docs/                         # Sphinx documentation site
│   ├── Makefile                  # Sphinx build makefile
│   ├── make.bat                  # Windows build batch script
│   ├── requirements-docs.txt     # Sphinx documentation dependencies
│   └── source/                   # Sphinx documentation source files
│       ├── conf.py               # Sphinx configuration
│       ├── index.rst             # Documentation home page
│       ├── _static/              # Architecture diagram & assets
│       ├── api/                  # API reference docs
│       ├── architecture/         # System architecture docs
│       ├── cicd/                 # CI/CD & Docker docs
│       ├── data/                 # Data schema docs
│       ├── developer/            # Developer guide docs
│       ├── getting-started/      # Installation & running docs
│       ├── monitoring/           # Monitoring docs
│       ├── rag/                  # RAG & AI docs
│       ├── security/             # Security docs
│       ├── testing/              # Pytest & benchmark docs
│       └── user-guide/           # Streamlit UI guide docs
├── src/                          # Application source code
│   ├── ai/                       # Vector store, retriever, RAG, LLM, embeddings, evaluation
│   ├── api/                      # FastAPI main app, router, Pydantic models
│   ├── ingestion/                # Document loader & ingestion pipeline
│   ├── processing/               # Text cleaner & chunker
│   └── utils/                    # Configuration, history, feedback, logging
├── tests/                        # Pytest suite (34 unit & integration tests)
├── app.py                        # Streamlit web application
├── Dockerfile                    # Container build definition
├── docker-compose.yml            # Docker Compose orchestration
├── sonar-project.properties      # SonarCloud configuration
├── requirements.txt              # Application Python dependencies
└── README.md                     # Repository README
```
