from pydantic import BaseModel, Field
from typing import List, Optional

class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    ollama_model: Optional[str] = Field(None, example="qwen2.5:1.5b")
    vector_store_status: Optional[str] = Field(None, example="ready")

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        example="What should be checked when an EV reports repeated battery overheating?",
        min_length=1
    )

class SourceMetadata(BaseModel):
    document: str = Field(..., example="sample_ev_battery_service.txt")
    page: int = Field(..., example=1)
    document_type: Optional[str] = Field(None, example="TXT")
    score: float = Field(..., example=0.85)
    chunk_id: Optional[str] = Field(None)

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

class DocumentListResponse(BaseModel):
    documents: List[DocumentItem]
    total_indexed_documents: int
