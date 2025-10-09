"""
Retriever Module
Handles document retrieval and re-ranking
"""

from typing import List
from langchain.schema import Document


class Retriever:
    """Retrieves and re-ranks relevant document chunks"""

    def __init__(self, vector_store, embedding_function, llm=None):
        """
        Initialize retriever

        Args:
            vector_store: VectorStore instance
            embedding_function: Embedding model
            llm: Language model for re-ranking (optional)
        """
        self.vector_store = vector_store
        self.embedding_function = embedding_function
        self.llm = llm

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieve top-k similar chunks for a query

        Args:
            query: User query string
            k: Number of chunks to retrieve

        Returns:
            List of relevant Document chunks
        """
        # Embed query
        query_vector = self.embedding_function.embed_query(query)

        # Retrieve similar chunks
        chunks = self.vector_store.similarity_search_by_vector(query_vector, k=k)
        return chunks

    def re_rank(
        self, query: str, retrieved_chunks: List[Document], top_k: int = 3
    ) -> List[Document]:
        """
        Re-rank chunks using LLM based on relevance

        Args:
            query: User query string
            retrieved_chunks: Initial retrieved chunks
            top_k: Number of top chunks to return after re-ranking

        Returns:
            Top-k re-ranked Document chunks
        """
        if self.llm is None:
            print("No LLM provided for re-ranking, returning original chunks")
            return retrieved_chunks[:top_k]

        scored_chunks = []

        for chunk in retrieved_chunks:
            # Create scoring prompt
            prompt = f"""
            Question: {query}

            Context Chunk (first 500 chars): {chunk.page_content[:500]}

            Rate the relevance of this chunk to the question on a scale from 0 (not relevant) to 10 (highly relevant).
            Only return the numeric score.
            """

            try:
                # Get relevance score from LLM
                score_str = self.llm.invoke(prompt)
                score = float(score_str.content.strip())
            except Exception as e:
                print(f"LLM scoring failed, defaulting score=0: {e}")
                score = 0.0

            scored_chunks.append((score, chunk))

        # Sort by relevance score (descending)
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        # Return top_k chunks
        top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]
        return top_chunks
