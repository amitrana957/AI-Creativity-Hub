from pathlib import Path
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models import hf_embeddings, gemini_llm

# 1. Load PDF
pdf_path = Path(__file__).parent.parent / "data" / "qa.pdf"
documents = UnstructuredPDFLoader(str(pdf_path)).load()

# 2. Split PDF into chunks
chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(documents)

# 3. Add metadata to each chunk
for i, chunk in enumerate(chunks):
    chunk.metadata = {"source": pdf_path.name, "chunk_index": i}

# 4. Store chunks in Chroma vector DB
vector_db = Chroma.from_documents(
    chunks, embedding=hf_embeddings, persist_directory="db/basic"
)

# 5. Take user question
user_question = "Who is Brian?"

# 6. Convert user question into embedding
query_vector = hf_embeddings.embed_query(user_question)

# 7. Retrieve top-k similar chunks from vector DB
top_chunks = vector_db.similarity_search_by_vector(query_vector, k=3)

# 8. Print top chunks and metadata
for i, chunk in enumerate(top_chunks, 1):
    print(f"--- Chunk {i} ---")
    print(chunk.page_content[:500])
    print("Metadata:", chunk.metadata)
    print()

# 9. Combine retrieved chunks into context
context = "\n\n".join([chunk.page_content for chunk in top_chunks])

# 10. Create prompt
prompt = f"""You are a helpful assistant. Use the context below to answer the user's question truthfully.
If the answer is not in the document, say "Information not available in the document."

Context:
{context}

Question: {user_question}

Answer:"""

# 11. Get response from LLM
response = gemini_llm.invoke(prompt)

print("\n--- FINAL ANSWER ---")
print(response.content)
