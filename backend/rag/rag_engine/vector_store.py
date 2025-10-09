"""
Vector Store Module
Manages Chroma vector database operations
"""

from pathlib import Path
from typing import List, Optional
from langchain_chroma import Chroma
from langchain.schema import Document


class VectorStore:
    """Manages vector database operations"""

    def __init__(self, db_folder: Path, embedding_function):
        """
        Initialize vector store

        Args:
            db_folder: Path to database folder
            embedding_function: Embedding model to use
        """
        self.db_folder = db_folder
        self.embedding_function = embedding_function
        self.vector_db: Optional[Chroma] = None

        # Initialize if database exists
        if (db_folder / "chroma.sqlite3").exists():
            self.vector_db = Chroma(
                persist_directory=str(db_folder), embedding_function=embedding_function
            )
            print(f"Loaded existing vector database from {db_folder}")

    def add_documents(self, chunks: List[Document]) -> None:
        """
        Add document chunks to vector database

        Args:
            chunks: List of Document chunks to add
        """
        if self.vector_db is None:
            # Initialize database with first documents
            self.vector_db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding_function,
                persist_directory=str(self.db_folder),
            )
            print(f"Created new vector database with {len(chunks)} chunks")
        else:
            # Add to existing database
            self.vector_db.add_documents(chunks)
            print(f"Added {len(chunks)} chunks to existing database")

    def similarity_search_by_vector(
        self, query_vector: List[float], k: int = 3
    ) -> List[Document]:
        """
        Search for similar documents using query vector

        Args:
            query_vector: Embedded query vector
            k: Number of results to return

        Returns:
            List of similar Document objects
        """
        if self.vector_db is None:
            raise ValueError("Vector database not initialized. Ingest documents first.")

        return self.vector_db.similarity_search_by_vector(query_vector, k=k)

    def is_initialized(self) -> bool:
        """Check if vector database is initialized"""
        return self.vector_db is not None
