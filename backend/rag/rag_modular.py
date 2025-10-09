"""
Main Application File
Example usage of the modular RAG pipeline
Place this file in the Backend root folder
"""

from pathlib import Path
from models import hf_embeddings, gemini_llm
from .rag_engine import RAGPipeline
from lib import pretty_print


def main():
    """Main function to run the RAG pipeline"""

    # ---------------- Configuration ----------------
    BASE_DIR = Path(__file__).resolve().parent.parent

    # PDF file path
    PDF_PATH = BASE_DIR / "data" / "qa.pdf"

    # Database folder
    DB_FOLDER = BASE_DIR / "db" / "modular"

    # ---------------- Initialize RAG Pipeline ----------------
    pipeline = RAGPipeline(
        db_folder=DB_FOLDER,
        embedding_function=hf_embeddings,
        llm=gemini_llm,
        chunk_size=1000,
        chunk_overlap=200,
    )

    # Check pipeline status
    status = pipeline.get_pipeline_status()
    print(f"Pipeline Status: {status}")

    # ---------------- Ingest Document ----------------
    print(f"\nIngesting document: {PDF_PATH}")
    success = pipeline.ingest_document(PDF_PATH)

    if success:
        print("✓ Document ingested successfully")
    else:
        print("ℹ Document already processed or ingestion failed")

    # ---------------- Query the Pipeline ----------------
    user_question = "What time does Brian usually get up?"

    print(f"\nQuerying: {user_question}")

    # Basic retrieval (without re-ranking)
    answer = pipeline.query(question=user_question, k=2, use_reranking=False)

    # Display results
    pretty_print(f"Question: {user_question}\n\nAnswer: {answer}")


if __name__ == "__main__":
    main()
