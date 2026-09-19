import requests
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, status, Query
from src.api.models import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
    IngestResponse,
    DocumentListResponse,
    DocumentItem,
    DeleteDocumentResponse,
    QueryHistoryResponse,
    QueryHistoryItem,
    EvaluationReport,
    BenchmarkDatasetResponse,
    TestCaseRequest,
    TestCaseResult,
    FeedbackRequest,
    FeedbackResponse
)
from src.ingestion.ingest import IngestionPipeline
from src.ai.vector_store import VectorStoreManager
from src.ai.retriever import ServiceKnowledgeRetriever
from src.ai.rag import RAGPipeline
from src.ai.evaluation import BENCHMARK_DATASET, evaluate_single_test_case, run_rag_evaluation
from src.utils.history import QueryHistoryManager, FeedbackManager
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("api_routes")

router = APIRouter()

# Global instances — single VectorStoreManager shared across ALL components
vector_store_manager = VectorStoreManager()
ingestion_pipeline = IngestionPipeline(vector_store_manager=vector_store_manager)
_shared_retriever = ServiceKnowledgeRetriever(vector_store_manager=vector_store_manager)
rag_pipeline = RAGPipeline(retriever=_shared_retriever)
history_manager = QueryHistoryManager()
feedback_manager = FeedbackManager()


@router.get("/health", response_model=HealthResponse, summary="Enhanced Health & Component Monitoring")
def health_check():
    """Returns live structured health and operational status for API, Vector Store, Embeddings, and Ollama connection."""
    vector_status = "ready" if vector_store_manager.vector_store is not None and vector_store_manager.get_total_chunks_count() > 0 else "no_index"
    doc_info = vector_store_manager.get_indexed_documents_info()
    docs_count = len(doc_info)
    chunks_count = vector_store_manager.get_total_chunks_count()

    embeddings_status = "ready" if vector_store_manager.embeddings is not None else "unavailable"

    ollama_status = "disconnected"
    try:
        res = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=2)
        if res.status_code == 200:
            ollama_status = "connected"
    except Exception:
        ollama_status = "disconnected"

    components = {
        "api": "healthy",
        "vector_store": "healthy" if vector_status == "ready" else "no_index",
        "embeddings": embeddings_status,
        "ollama": "healthy" if ollama_status == "connected" else "disconnected",
        "llm": settings.OLLAMA_MODEL
    }

    overall_status = "healthy" if ollama_status == "connected" and vector_status == "ready" else "degraded"

    return HealthResponse(
        status="ok",
        api="healthy",
        vector_store=vector_status,
        embeddings=embeddings_status,
        ollama=ollama_status,
        llm=settings.OLLAMA_MODEL,
        documents_count=docs_count,
        chunks_count=chunks_count,
        components=components
    )


@router.post("/ingest", response_model=IngestResponse, summary="Trigger Knowledge Base Ingestion")
def ingest_documents():
    """Ingests all files from the sample data directory into the vector store."""
    try:
        result = ingestion_pipeline.run(source_dir=settings.DATA_SAMPLE_DIR)
        return IngestResponse(
            status=result["status"],
            message=result["message"],
            documents_count=result.get("documents_count", 0),
            chunks_count=result.get("chunks_count", 0)
        )
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion pipeline error: {str(e)}"
        )


@router.post("/upload", response_model=IngestResponse, summary="Upload & Ingest Multi-Format Document")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a PDF, TXT, DOCX, or CSV document safely, saves it to data/uploads, and indexes it."""
    allowed_extensions = {".pdf", ".txt", ".docx", ".csv"}
    filename = file.filename or ""

    # Path traversal prevention & filename sanitization
    safe_name = Path(filename).name
    if not safe_name or safe_name != filename or ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or malicious filename provided."
        )

    ext = Path(safe_name).suffix.lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(allowed_extensions)}"
        )

    try:
        content = await file.read()
        max_bytes = 10 * 1024 * 1024  # 10 MB limit
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum allowed limit of 10MB."
            )

        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        target_path = settings.DATA_UPLOAD_DIR / safe_name
        with open(target_path, "wb") as f:
            f.write(content)

        logger.info(f"Saved uploaded file to {target_path} ({len(content)} bytes)")

        result = ingestion_pipeline.ingest_single_file(target_path)
        return IngestResponse(
            status=result["status"],
            message=result["message"],
            documents_count=1,
            chunks_count=result.get("chunks_count", 0)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling upload for {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process uploaded file: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse, summary="Query BMW Service Knowledge RAG")
def query_rag(request: QueryRequest):
    """Submits a technical question to the RAG pipeline and returns a grounded answer with deduplicated sources."""
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question field cannot be empty."
        )

    try:
        response = rag_pipeline.answer_question(
            question=question,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold
        )
        return QueryResponse(
            question=response["question"],
            answer=response["answer"],
            sources=response["sources"],
            grounding=response.get("grounding", "HIGH"),
            sources_count=response.get("sources_count", len(response["sources"]))
        )
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG query: {str(e)}"
        )


@router.post("/feedback", response_model=FeedbackResponse, summary="Submit User Feedback on RAG Answer")
def submit_feedback(request: FeedbackRequest):
    """Records technician user feedback (thumbs up/down) for an answer."""
    try:
        feedback_manager.add_feedback(
            query=request.query,
            answer=request.answer,
            helpful=request.helpful,
            reason=request.reason,
            comments=request.comments
        )
        return FeedbackResponse(
            status="success",
            message="Feedback recorded successfully."
        )
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record feedback: {str(e)}"
        )


@router.get("/documents", response_model=DocumentListResponse, summary="List Indexed Documents")
def list_documents():
    """Returns a list of all document files currently indexed in the FAISS vector store."""
    try:
        doc_info = vector_store_manager.get_indexed_documents_info()
        items = [DocumentItem(**item) for item in doc_info]
        return DocumentListResponse(
            documents=items,
            total_indexed_documents=len(items)
        )
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document metadata: {str(e)}"
        )


@router.delete("/documents/{filename}", response_model=DeleteDocumentResponse, summary="Delete Document & Rebuild Vector Store")
def delete_document(filename: str):
    """Deletes a document and rebuilds the FAISS vector index safely."""
    try:
        success, chunks_removed, target_filename = vector_store_manager.delete_document(filename)
        if not success or chunks_removed == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{filename}' not found in vector store."
            )
        return DeleteDocumentResponse(
            status="success",
            message=f"Document '{target_filename}' deleted successfully.",
            document=target_filename,
            chunks_removed=chunks_removed
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )


@router.get("/history", response_model=QueryHistoryResponse, summary="Retrieve Local Query History")
def get_query_history(limit: int = Query(50, ge=1, le=100)):
    """Returns recent technician query execution history."""
    try:
        history = history_manager.get_history(limit=limit)
        items = [QueryHistoryItem(**item) for item in history]
        return QueryHistoryResponse(
            history=items,
            total_records=len(items)
        )
    except Exception as e:
        logger.error(f"Error fetching query history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch query history: {str(e)}"
        )


@router.get("/evaluate/dataset", response_model=BenchmarkDatasetResponse, summary="Retrieve Evaluation Benchmark Dataset")
def get_evaluation_dataset():
    """Returns the list of benchmark dataset test case definitions."""
    return BenchmarkDatasetResponse(dataset=BENCHMARK_DATASET)


@router.post("/evaluate/test-case", response_model=TestCaseResult, summary="Evaluate Single Benchmark Test Case")
def evaluate_test_case(request: TestCaseRequest):
    """Evaluates a single benchmark test case through the production RAG pipeline with per-item error handling."""
    try:
        test_case_dict = request.dict()
        res = evaluate_single_test_case(test_case_dict, rag_pipeline=rag_pipeline)
        return TestCaseResult(**res)
    except Exception as e:
        logger.error(f"Error evaluating test case {request.id}: {e}")
        return TestCaseResult(
            id=request.id,
            question=request.question,
            expected_document=request.expected_document or "N/A",
            retrieved_documents=[],
            retrieval_success=False,
            number_of_sources=0,
            answer_generated=f"ERROR: {str(e)}",
            fallback_expected=request.expect_fallback,
            fallback_returned=False,
            status="ERROR",
            passed=False,
            error=str(e),
            evaluation_note=f"API handler error: {str(e)}"
        )


@router.get("/evaluate", response_model=EvaluationReport, summary="Run Full RAG Evaluation Benchmark Suite")
def evaluate_rag():
    """Executes automated evaluation benchmark test suite against current RAG system."""
    try:
        report = run_rag_evaluation(rag_pipeline=rag_pipeline)
        return EvaluationReport(**report)
    except Exception as e:
        logger.error(f"Error running RAG evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )
