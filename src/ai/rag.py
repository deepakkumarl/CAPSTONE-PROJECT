from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from src.ai.retriever import ServiceKnowledgeRetriever
from src.ai.llm import get_llm
from src.utils.history import QueryHistoryManager
from src.utils.logging_config import setup_logger

logger = setup_logger("rag")

FALLBACK_RESPONSE = "I could not find sufficient information in the available BMW service documentation."

SYSTEM_PROMPT = """You are a BMW service documentation assistant.

Answer ONLY using the provided context.

Do not use outside knowledge.

If the context does not contain enough information to answer the question, say that the available documentation does not contain sufficient information.

Do not invent procedures, specifications, diagnostic steps, torque values, safety instructions, or component information.

If only part of the question is supported by the context, answer only the supported portion and clearly state what is not available.

When possible, cite the source document and page number.

Context:
{context}
"""

class RAGPipeline:
    """End-to-end RAG orchestrator combining FAISS retrieval, query history, and local Ollama generation."""

    def __init__(self, retriever: ServiceKnowledgeRetriever = None):
        self.retriever = retriever or ServiceKnowledgeRetriever()
        self.history_manager = QueryHistoryManager()
        self.llm = None
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}")
        ])

    def _init_llm(self):
        if self.llm is None:
            self.llm = get_llm()

    def answer_question(
        self,
        question: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes the RAG pipeline:
        1. Validates input
        2. Retrieves top relevant chunks from FAISS (deduplicated)
        3. If no relevant context found, returns fallback response
        4. Constructs grounded prompt and invokes Ollama
        5. Logs query to local history
        6. Returns answer and unique source metadata
        """
        if not question or not question.strip():
            return {
                "question": question,
                "answer": "Please provide a valid diagnostic service question.",
                "sources": []
            }

        logger.info(f"Processing RAG query: '{question}'")

        # Step 1 & 2: Retrieval & Relevance Validation
        if top_k is not None or similarity_threshold is not None:
            docs, sources = self.retriever.retrieve(
                query=question,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
        else:
            docs, sources = self.retriever.retrieve(question)

        if not docs:
            logger.info("Retrieval returned no relevant documents above similarity threshold.")
            result = {
                "question": question,
                "answer": FALLBACK_RESPONSE,
                "sources": [],
                "grounding": "INSUFFICIENT",
                "sources_count": 0
            }
            self.history_manager.add_entry(
                question=question,
                answer=FALLBACK_RESPONSE,
                sources=[],
                status="fallback"
            )
            return result

        top_score = max([s.get("score", 0.0) for s in sources]) if sources else 0.0
        grounding_level = "HIGH" if top_score >= 0.60 else "MEDIUM"

        # Step 3: Format context
        context_str = "\n\n---\n\n".join([
            f"[Source: {d.metadata.get('source', 'Doc')} | Page: {d.metadata.get('page', 1)}]\n{d.page_content}"
            for d in docs
        ])

        # Step 4: Prompt Construction & LLM Execution
        try:
            self._init_llm()
            messages = self.prompt_template.format_messages(
                context=context_str,
                question=question
            )
            logger.info(f"Sending prompt to local Ollama model with {len(docs)} context chunks...")
            response = self.llm.invoke(messages)
            answer_text = response.content if hasattr(response, "content") else str(response)
            clean_answer = answer_text.strip()

            result = {
                "question": question,
                "answer": clean_answer,
                "sources": sources,
                "grounding": grounding_level,
                "sources_count": len(sources)
            }

            self.history_manager.add_entry(
                question=question,
                answer=clean_answer,
                sources=sources,
                status="success"
            )

            logger.info(f"Successfully generated grounded answer from Ollama (Grounding: {grounding_level}).")
            return result

        except Exception as e:
            logger.error(f"Failed to generate answer from Ollama LLM: {e}")
            error_answer = f"Error communicating with local LLM (Ollama): {str(e)}. Please ensure Ollama is running."
            result = {
                "question": question,
                "answer": error_answer,
                "sources": sources,
                "grounding": "INSUFFICIENT",
                "sources_count": len(sources)
            }
            self.history_manager.add_entry(
                question=question,
                answer=error_answer,
                sources=sources,
                status="error"
            )
            return result
