"""
Document Loader Module
Handles PDF loading with fallback mechanisms
"""

from pathlib import Path
from typing import List
from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.schema import Document


class DocumentLoader:
    """Loads PDF documents with automatic fallback"""

    def __init__(self):
        self.loader_name = None

    def load_pdf(self, pdf_path: Path) -> List[Document]:
        """
        Load a PDF file using UnstructuredPDFLoader with PyPDFLoader fallback

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of Document objects
        """
        try:
            loader = UnstructuredPDFLoader(str(pdf_path))
            documents = loader.load()
            self.loader_name = "UnstructuredPDFLoader"
            print(
                f"Loaded {len(documents)} pages from {pdf_path.name} using {self.loader_name}"
            )
            return documents
        except Exception as e:
            print(
                f"UnstructuredPDFLoader failed for {pdf_path.name}, falling back to PyPDFLoader: {e}"
            )
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
            self.loader_name = "PyPDFLoader"
            print(
                f"Loaded {len(documents)} pages from {pdf_path.name} using {self.loader_name}"
            )
            return documents
