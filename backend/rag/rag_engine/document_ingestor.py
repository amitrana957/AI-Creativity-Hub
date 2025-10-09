"""
Document Ingestor Module
Orchestrates document loading, chunking, and ingestion into vector store
"""

from pathlib import Path
from shutil import copy2
from .document_loader import DocumentLoader
from .text_chunker import TextChunker
from .vector_store import VectorStore


class DocumentIngestor:
    """Orchestrates PDF ingestion pipeline"""

    def __init__(
        self,
        vector_store: VectorStore,
        processed_folder: Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize document ingestor

        Args:
            vector_store: VectorStore instance
            processed_folder: Folder to store processed PDFs
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.vector_store = vector_store
        self.processed_folder = processed_folder
        self.loader = DocumentLoader()
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # Ensure processed folder exists
        self.processed_folder.mkdir(parents=True, exist_ok=True)

    def is_already_processed(self, pdf_path: Path) -> bool:
        """
        Check if PDF has already been processed

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if already processed, False otherwise
        """
        processed_file = self.processed_folder / pdf_path.name
        return processed_file.exists()

    def ingest_pdf(self, pdf_path: Path) -> bool:
        """
        Ingest a single PDF into the vector database

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if ingestion successful, False if skipped or failed
        """
        # Check if already processed
        if self.is_already_processed(pdf_path):
            print(f"{pdf_path.name} already processed. Skipping ingestion.")
            return False

        try:
            # Step 1: Load PDF
            documents = self.loader.load_pdf(pdf_path)

            # Step 2: Chunk documents
            chunks = self.chunker.chunk_documents(documents, pdf_path.name)

            # Step 3: Add to vector store
            self.vector_store.add_documents(chunks)

            # Step 4: Mark as processed
            processed_file = self.processed_folder / pdf_path.name
            copy2(pdf_path, processed_file)
            print(
                f"{pdf_path.name} ingested successfully and copied to {processed_file}"
            )

            return True

        except Exception as e:
            print(f"Failed to ingest {pdf_path.name}: {e}")
            return False
