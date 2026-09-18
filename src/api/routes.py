from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from src.api.models import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
    IngestResponse,
    DocumentListResponse,
    DocumentItem
)
from src.ingestion.ingest import IngestionPipeline
from src.ai.vector_store import VectorStoreManager
from src.ai.rag import RAGPipeline
from src.utils.config import settings
from src.utils.logging_config import setup_logger

logger = setup_logger("api_routes")

router = APIRouter()

# Global instances (lazy initialized)
vector_store_manager = VectorStoreManager()
ingestion_pipeline = IngestionPipeline(vector_store_manager=vector_store_manager)
rag_pipeline = RAGPipeline()


@router.get("/health", response_model=HealthResponse, summary="Health Check")
def health_check():
    """Returns the operational status of the API service."""
    vector_status = "ready" if vector_store_manager.vector_store is not None else "no_index"
    return HealthResponse(
        status="ok",
        ollama_model=settings.OLLAMA_MODEL,
        vector_store_status=vector_status
    )


@router.post("/ingest", response_model=IngestResponse, summary="Trigger Document Ingestion")
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


@router.post("/upload", response_model=IngestResponse, summary="Upload and Ingest Document")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a PDF, TXT, or DOCX document, saves it to data/uploads, and indexes it."""
    allowed_extensions = {".pdf", ".txt", ".docx", ".csv"}
    filename = file.filename
    ext = Path(filename).suffix.lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(allowed_extensions)}"
        )

    try:
        # Sanitize filename
        safe_name = Path(filename).name
        target_path = settings.DATA_UPLOAD_DIR / safe_name

        # Save uploaded file
        with open(target_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"Saved uploaded file to {target_path}")

        # Ingest single file
        result = ingestion_pipeline.ingest_single_file(target_path)
        return IngestResponse(
            status=result["status"],
            message=result["message"],
            documents_count=1,
            chunks_count=result.get("chunks_count", 0)
        )
    except Exception as e:
        logger.error(f"Error handling upload for {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process uploaded file: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse, summary="Query BMW Service Documentation RAG")
def query_rag(request: QueryRequest):
    """Submits a technical question to the RAG pipeline and returns a grounded answer with sources."""
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question field cannot be empty."
        )

    try:
        response = rag_pipeline.answer_question(question)
        return QueryResponse(
            question=response["question"],
            answer=response["answer"],
            sources=response["sources"]
        )
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG query: {str(e)}"
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
