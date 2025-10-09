"""
RAG Pipeline Module
Main orchestration class that brings all components together
"""

from pathlib import Path
from typing import Optional
from .vector_store import VectorStore
from .document_ingestor import DocumentIngestor
from .retriever import Retriever
from .answer_generator import AnswerGenerator


class RAGPipeline:
    """Complete RAG pipeline orchestrator"""

    def __init__(
        self,
        db_folder: Path,
        embedding_function,
        llm,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize RAG pipeline with all components

        Args:
            db_folder: Path to vector database folder
            embedding_function: Embedding model
            llm: Language model for generation
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        # Initialize folders
        self.db_folder = db_folder
        self.processed_folder = db_folder / "processed"
        self.db_folder.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.vector_store = VectorStore(db_folder, embedding_function)
        self.ingestor = DocumentIngestor(
            vector_store=self.vector_store,
            processed_folder=self.processed_folder,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.retriever = Retriever(
            vector_store=self.vector_store,
            embedding_function=embedding_function,
            llm=llm,
        )
        self.generator = AnswerGenerator(llm=llm)

        print(f"RAG Pipeline initialized with database at {db_folder}")

    def ingest_document(self, pdf_path: Path) -> bool:
        """
        Ingest a PDF document into the pipeline

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if successful, False otherwise
        """
        return self.ingestor.ingest_pdf(pdf_path)

    def query(
        self,
        question: str,
        k: int = 3,
        use_reranking: bool = False,
        rerank_top_k: Optional[int] = None,
    ) -> str:
        """
        Query the RAG pipeline

        Args:
            question: User question
            k: Number of chunks to retrieve
            use_reranking: Whether to use LLM-based re-ranking
            rerank_top_k: Number of chunks to keep after re-ranking

        Returns:
            Generated answer string
        """
        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(question, k=k)

        # Optional re-ranking
        if use_reranking:
            top_k = rerank_top_k if rerank_top_k else k
            chunks = self.retriever.re_rank(question, chunks, top_k=top_k)

        # Generate answer
        answer = self.generator.generate_answer(question, chunks)

        return answer

    def get_pipeline_status(self) -> dict:
        """
        Get status of pipeline components

        Returns:
            Dictionary with status information
        """
        return {
            "vector_db_initialized": self.vector_store.is_initialized(),
            "db_folder": str(self.db_folder),
            "processed_folder": str(self.processed_folder),
        }
