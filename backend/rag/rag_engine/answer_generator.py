"""
Answer Generator Module
Generates answers using LLM and retrieved context
"""

import re
from typing import List
from langchain.schema import Document
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class AnswerGenerator:
    """Generates answers from retrieved context using LLM"""

    def __init__(self, llm):
        """
        Initialize answer generator

        Args:
            llm: Language model for answer generation
        """
        self.llm = llm

        # Define prompt templates
        self.system_template = (
            "You are an expert assistant. Use the context provided to answer questions accurately. "
            "Include all relevant details from the context. "
            "If the answer is not in the context, say 'I don't know'."
        )

        self.human_template = (
            "Context:\n{context}\n\n"
            "Question:\n{query}\n\n"
            "Answer the question using all the context above. "
            "Write full sentences and do not omit any relevant information."
        )

    def clean_chunk_text(self, text: str) -> str:
        """
        Clean chunk text by removing extra whitespace and headers

        Args:
            text: Raw chunk text

        Returns:
            Cleaned text
        """
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

    def format_context(self, chunks: List[Document]) -> str:
        """
        Format retrieved chunks into context string

        Args:
            chunks: List of Document chunks

        Returns:
            Formatted context string
        """
        context_text = ""

        for chunk in chunks:
            src = chunk.metadata.get("source", "unknown")
            idx = chunk.metadata.get("chunk_index", "?")

            # Clean full content
            full_content = self.clean_chunk_text(chunk.page_content)

            # Take first 50 words as preview
            preview = " ".join(full_content.split()[:50])

            # Add to context
            context_text += (
                f"[{src}, chunk {idx}] Preview: {preview}\n"
                f"Full Content:\n{full_content}\n\n"
            )

        return context_text

    def generate_answer(self, query: str, chunks: List[Document]) -> str:
        """
        Generate answer using LLM and retrieved context

        Args:
            query: User query string
            chunks: Retrieved document chunks

        Returns:
            Generated answer string
        """
        # Format context from chunks
        context_text = self.format_context(chunks)

        # Create prompt template
        system_msg = SystemMessagePromptTemplate.from_template(self.system_template)
        human_msg = HumanMessagePromptTemplate.from_template(self.human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])

        # Format messages
        formatted_messages = chat_prompt.format_messages(
            context=context_text, query=query
        )

        # Call LLM
        try:
            response = self.llm.invoke(formatted_messages)
            return response.content.strip()
        except Exception as e:
            print(f"LLM call failed: {e}")
            return "Error: Unable to generate answer."
