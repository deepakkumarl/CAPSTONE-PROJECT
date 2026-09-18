from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    api: str = Field(..., example="healthy")
    vector_store: str = Field(..., example="ready")
    embeddings: str = Field(..., example="ready")
    ollama: str = Field(..., example="connected")
    llm: str = Field(..., example="qwen2.5:1.5b")
    documents_count: int = Field(..., example=3)
    chunks_count: int = Field(..., example=12)

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        example="What should be checked when an EV reports repeated battery overheating?",
        min_length=1
    )
    top_k: Optional[int] = Field(None, example=5, ge=1, le=20)
    similarity_threshold: Optional[float] = Field(None, example=0.35, ge=0.0, le=1.0)

class SourceMetadata(BaseModel):
    document: str = Field(..., example="sample_ev_battery_service.txt")
    page: int = Field(..., example=1)
    document_type: Optional[str] = Field(None, example="TXT")
    score: float = Field(..., example=0.88)
    chunk_id: Optional[str] = Field(None)
    snippet: Optional[str] = Field(None)

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceMetadata]

class IngestResponse(BaseModel):
    status: str
    message: str
    documents_count: int
    chunks_count: int

class DocumentItem(BaseModel):
    filename: str
    document_type: str
    total_chunks: int
    pages_count: int
    status: str = "Indexed"

class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]
    total_indexed_documents: int

class DeleteDocumentResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="Document deleted successfully")
    document: str = Field(..., example="sample_ev_battery_service.txt")
    chunks_removed: int = Field(..., example=6)

class QueryHistoryItem(BaseModel):
    timestamp: str
    question: str
    answer: str
    retrieved_documents: List[str]
    sources_count: int
    status: str
    sources: List[SourceMetadata]

class QueryHistoryResponse(BaseModel):
    history: List[QueryHistoryItem]
    total_records: int

class TestCaseRequest(BaseModel):
    id: str = Field(..., example="TC-001")
    question: str = Field(..., example="What should be checked when an EV reports repeated battery overheating?")
    expected_document: Optional[str] = Field(None, example="sample_ev_battery_service.txt")
    expect_fallback: bool = Field(False, example=False)

class TestCaseResult(BaseModel):
    id: str
    question: str
    expected_document: str
    retrieved_documents: List[str]
    retrieval_success: bool
    number_of_sources: int
    answer_generated: str
    fallback_expected: bool
    fallback_returned: bool
    status: str
    passed: bool
    error: Optional[str] = None
    evaluation_note: str

class BenchmarkDatasetResponse(BaseModel):
    dataset: List[Dict[str, Any]]

class EvaluationReport(BaseModel):
    summary: Dict[str, Any]
    details: List[TestCaseResult]
