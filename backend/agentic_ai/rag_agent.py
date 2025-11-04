from pathlib import Path
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from models import hf_embeddings, gemini_llm
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# -------------------- Vector DB --------------------
pdf_path = Path(__file__).parent.parent / "data" / "qa.pdf"
persist_dir = Path("db/basic")

if not persist_dir.exists():
    print("🔍 Creating new Chroma vector store...")
    documents = UnstructuredPDFLoader(str(pdf_path)).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    ).split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata = {"source": pdf_path.name, "chunk_index": i}

    vector_db = Chroma.from_documents(
        chunks, embedding=hf_embeddings, persist_directory=str(persist_dir)
    )
else:
    print("📦 Loading existing Chroma vector store...")
    vector_db = Chroma(
        persist_directory=str(persist_dir), embedding_function=hf_embeddings
    )


# -------------------- Tool --------------------
@tool
def retrieve_from_db(query: str):
    """Retrieve relevant text chunks from the document database."""
    query_vector = hf_embeddings.embed_query(query)
    results = vector_db.similarity_search_by_vector(query_vector, k=3)
    context = "\n\n".join([doc.page_content for doc in results])
    return context


# -------------------- Prompt --------------------
prompt = PromptTemplate.from_template(
    """
You are a helpful assistant specialized in answering questions from documents.

You have access to the following tools:
{tools}

Follow this reasoning process:
1. Think about whether you need to look up information.
2. If yes, call the appropriate tool with a natural language query.
3. Once you have the context, answer concisely using that information.
4. If the document doesn't contain the answer, say: "Information not available in the document."

Question: {input}

{agent_scratchpad}
"""
)

# -------------------- Agent --------------------
agent = create_react_agent(
    model=gemini_llm,
    tools=[retrieve_from_db],
    prompt=prompt,
)

# -------------------- Run --------------------
user_question = "Who is Brian?"
response = agent.invoke({"messages": [HumanMessage(content=user_question)]})

for m in response["messages"]:
    m.pretty_print()
