"""
Text Chunker Module
Handles document splitting and metadata management
"""

from typing import List
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class TextChunker:
    """Splits documents into chunks with metadata"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker

        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk_documents(
        self, documents: List[Document], source_name: str
    ) -> List[Document]:
        """
        Split documents into chunks and add metadata

        Args:
            documents: List of Document objects to split
            source_name: Name of the source file for metadata

        Returns:
            List of chunked Document objects with metadata
        """
        chunks = self.splitter.split_documents(documents=documents)
        print(f"Created {len(chunks)} chunks for {source_name}")

        # Add metadata to each chunk
        for i, chunk in enumerate(chunks):
            if chunk.metadata is None:
                chunk.metadata = {}
            chunk.metadata.update({"source": source_name, "chunk_index": i})

        return chunks
