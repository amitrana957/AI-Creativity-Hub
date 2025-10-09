from pathlib import Path
from shutil import copy2
from langchain_community.document_loaders import UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models import hf_embeddings, gemini_llm
from lib import pretty_print
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


# ---------------- Paths ----------------
BASE_DIR = Path(__file__).resolve().parent.parent  # adjust .parent/.parent as needed

PDF_PATH = BASE_DIR / "data" / "qa.pdf"

DB_FOLDER = BASE_DIR / "db" / "pdf"

PROCESSED_FOLDER = DB_FOLDER / "processed"
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

# ---------------- Initialize vector DB if exists ----------------
vector_db = (
    Chroma(persist_directory=str(DB_FOLDER), embedding_function=hf_embeddings)
    if (DB_FOLDER / "chroma.sqlite3").exists()
    else None
)


# ---------------- Function to ingest a single PDF ----------------
def ingest_pdf(pdf_path: Path):
    """Ingest a single PDF into Chroma vector DB with metadata."""
    processed_file = PROCESSED_FOLDER / pdf_path.name
    if processed_file.exists():
        print(f"{pdf_path.name} already processed. Skipping ingestion.")
        return

    # Load PDF
    try:
        loader = UnstructuredPDFLoader(str(pdf_path))
        documents = loader.load()
        print(
            f"Loaded {len(documents)} pages from {pdf_path.name} using UnstructuredPDFLoader"
        )
    except Exception as e:
        print(
            f"UnstructuredPDFLoader failed for {pdf_path.name}, falling back to PyPDFLoader:",
            e,
        )
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from {pdf_path.name} using PyPDFLoader")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents=documents)
    print(f"Created {len(chunks)} chunks for {pdf_path.name}")

    # Add metadata for each chunk
    for i, chunk in enumerate(chunks):
        if chunk.metadata is None:
            chunk.metadata = {}
        chunk.metadata.update({"source": pdf_path.name, "chunk_index": i})

    # Initialize DB if first file
    global vector_db
    if vector_db is None:
        vector_db = Chroma.from_documents(
            documents=chunks, embedding=hf_embeddings, persist_directory=str(DB_FOLDER)
        )
    else:
        vector_db.add_documents(chunks)

    # Move PDF to processed folder
    copy2(pdf_path, processed_file)
    print(f"{pdf_path.name} ingested with metadata and copied to {processed_file}")


# ---------------- Embed user question ----------------
def embed_query(query: str):
    """Convert user query into embedding vector using the same model as documents."""
    try:
        return hf_embeddings.embed_query(query)
    except Exception as e:
        print("Embedding failed:", e)
        return None


# ---------------- Retrieve top-k chunks ----------------
def retrieve_top_chunks(query_vector, k=3):
    """
    Retrieve top-k most similar document chunks from Chroma
    using the query embedding.
    """
    if vector_db is None:
        raise ValueError("Vector DB not initialized. Ingest PDF first.")

    # Chroma method to search by vector
    results = vector_db.similarity_search_by_vector(query_vector, k=k)
    return results


# ---------------- Re-ranking top chunks ----------------
def re_rank_chunks(query: str, retrieved_chunks, top_k=3):
    """
    Re-rank chunks using an LLM based on query relevance.

    Parameters:
    - query: str → User’s question
    - retrieved_chunks: List[Document] → Chunks retrieved from vector DB
    - top_k: int → Number of final chunks to return after re-ranking

    Returns:
    - List[Document] → Top-k most relevant chunks
    """
    scored_chunks = []

    for chunk in retrieved_chunks:
        # ---------------- Create a scoring prompt ----------------
        prompt = f"""
        Question: {query}

        Context Chunk (first 500 chars): {chunk.page_content[:500]}

        Rate the relevance of this chunk to the question on a scale from 0 (not relevant) to 10 (highly relevant).
        Only return the numeric score.
        """
        try:
            # Call the LLM to get relevance score
            score_str = gemini_llm.invoke(prompt)
            score = float(score_str.content.strip())
        except Exception as e:
            print("LLM scoring failed, defaulting score=0:", e)
            score = 0.0

        scored_chunks.append((score, chunk))

    # ---------------- Sort by relevance score descending ----------------
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # ---------------- Return top_k chunks ----------------
    top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]
    return top_chunks


def clean_chunk_text(text):
    import re

    # Replace multiple newlines with single space
    text = re.sub(r"\n+", " ", text)
    # Remove unwanted headers (if consistent)
    text = re.sub(
        r"\b(Tokenizer|Parser|SAMPLE TEXT|Name Finder|POS Tagger|PRE PROCESSOR)\b",
        "",
        text,
    )
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def llm_answer(query: str, top_chunks, llm=gemini_llm) -> str:
    """
    Generate RAG answer using ChatPromptTemplate (proper kwargs for format_messages)
    """

    # Combine chunks into context
    context_text = ""
    for chunk in top_chunks:
        src = chunk.metadata.get("source", "unknown")
        idx = chunk.metadata.get("chunk_index", "?")

        # Clean full content
        full_content = clean_chunk_text(chunk.page_content)

        # Take first 50 words as preview
        preview = " ".join(full_content.split()[:50])

        # Add to context
        context_text += f"[{src}, chunk {idx}] Preview: {preview}\nFull Content:\n{full_content}\n\n"

    # System message
    system_msg = SystemMessagePromptTemplate.from_template(
        "You are an expert assistant. Use the context provided to answer questions accurately. "
        "Include all relevant details from the context. "
        "If the answer is not in the context, say 'I don't know'."
    )

    # Human message
    human_msg = HumanMessagePromptTemplate.from_template(
        "Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer the question using all the context above. "
        "Write full sentences and do not omit any relevant information."
    )

    # ChatPromptTemplate
    chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])

    # Format messages using kwargs (not a dict)
    formatted_messages = chat_prompt.format_messages(context=context_text, query=query)

    # Call LLM
    try:
        response = llm.invoke(formatted_messages)
        return response.content.strip()
    except Exception as e:
        print("LLM call failed:", e)
        return "Error: Unable to generate answer."


ingest_pdf(PDF_PATH)

user_question = "What time does Brian usually get up?"
query_vector = hf_embeddings.embed_query(user_question)

# Step 1: Coarse retrieval from Chroma
chunks = retrieve_top_chunks(query_vector, k=2)

# # Step 2: Re-rank using LLM ---> SKIP FOR NOW
# chunks = re_rank_chunks(user_question, chunks, top_k=3)

final_answer = llm_answer(query=user_question, top_chunks=chunks, llm=gemini_llm)

pretty_print(f"Question: {user_question}\n\nAnswer: {final_answer}")
