BMW Service Knowledge RAG
=========================

.. image:: https://img.shields.io/badge/Python-3.11-blue.svg
   :target: https://www.python.org/
.. image:: https://img.shields.io/badge/FastAPI-0.100+-green.svg
   :target: https://fastapi.tiangolo.com/
.. image:: https://img.shields.io/badge/Streamlit-1.25+-red.svg
   :target: https://streamlit.io/
.. image:: https://img.shields.io/badge/FAISS-CPU-orange.svg
   :target: https://github.com/facebookresearch/faiss
.. image:: https://img.shields.io/badge/Ollama-qwen2.5:1.5b-purple.svg
   :target: https://ollama.ai/
.. image:: https://img.shields.io/badge/Docker-deepakkumar889%2Fbmw--service--rag-blue.svg
   :target: https://hub.docker.com/r/deepakkumar889/bmw-service-rag

**Enterprise Local Retrieval-Augmented Generation (RAG) Platform for BMW Service Engineering**

The **BMW Service Knowledge RAG** platform provides automotive service technicians with instant, grounded access to technical manuals, diagnostic flowcharts, EV battery service procedures, and thermal management specifications. Operating 100% locally with zero cloud dependencies, it ensures complete data privacy and high diagnostic reliability.

Key Capabilities
----------------
* **Multi-Format Document Ingestion**: Native parsing for PDF, TXT, DOCX, and CSV documentation.
* **Grounded LLM Inferences**: Inferences generated using local Ollama ``qwen2.5:1.5b`` model with strict system prompts preventing hallucinations.
* **FAISS Vector Search**: Fast similarity search using ``sentence-transformers/all-MiniLM-L6-v2`` embeddings (384 dimensions).
* **Source Deduplication & Citations**: Precise source tracking by document name, file type, page number, and chunk ID.
* **Safe Document Deletion**: Full vector index reconstruction on document removal preserving stable metadata mappings.
* **Technician Feedback**: Interactive thumbs up/down feedback widget with JSON persistence.
* **Component Health Monitoring**: Real-time operational monitoring for API, FAISS, Embeddings, Ollama, and LLM dependencies.
* **Automated Evaluation Benchmark**: Built-in test suite evaluating retrieval accuracy and fallback triggers.

Architecture Overview
---------------------

.. image:: _static/architecture.png
   :width: 100%
   :alt: BMW Service Knowledge RAG Architecture Diagram

Quick Start
-----------

1. **Clone & Install Dependencies**:

   .. code-block:: bash

      git clone https://github.com/deepakkumar889/bmw-capstone-usecase.git
      cd bmw-capstone-usecase
      python -m venv .venv
      .venv\Scripts\Activate.ps1   # On Windows
      pip install -r requirements.txt

2. **Start Local Ollama Model**:

   .. code-block:: bash

      ollama pull qwen2.5:1.5b

3. **Run Backend API & Frontend**:

   .. code-block:: bash

      uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
      streamlit run app.py

Documentation Navigation
------------------------

.. toctree::
   :maxdepth: 2
   :caption: Navigation

   getting-started/index
   architecture/index
   user-guide/index
   api/index
   rag/index
   data/index
   testing/index
   security/index
   cicd/index
   monitoring/index
   developer/index

Indices and Tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
