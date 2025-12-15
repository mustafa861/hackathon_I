"""
RAG (Retrieval-Augmented Generation) pipeline for the chatbot.
"""

import asyncio
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
import os
from ..core.qdrant import get_qdrant_client

# Configuration
COLLECTION_NAME = "book_content_embeddings"
MAX_CONTEXT_LENGTH = 2000  # Maximum number of characters to send as context

class RAGPipeline:
    def __init__(self):
        self.qdrant_client = get_qdrant_client()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.collection_name = COLLECTION_NAME
        self.assistant_id = None
        self._initialize_assistant()

    def _initialize_assistant(self):
        """
        Initialize the OpenAI assistant. In a real application, you might want to
        create the assistant once and store its ID in a config or database.
        """
        # For this implementation, we'll create the assistant if it doesn't exist
        # In a real app, you would create it once and reuse the ID
        try:
            # Attempt to get an existing assistant by listing and filtering
            # For simplicity here, we'll just create a new one each time the app starts
            # In practice, you'd store the assistant ID somewhere persistent
            assistant = self.openai_client.beta.assistants.create(
                name="Physical AI & Humanoid Robotics Assistant",
                instructions=(
                    "You are an AI assistant for the 'Physical AI & Humanoid Robotics' book. "
                    "Answer questions based on the provided context from the book. "
                    "If the context doesn't contain enough information, say so."
                ),
                model="gpt-3.5-turbo",  # Or another appropriate model
            )
            self.assistant_id = assistant.id
        except Exception as e:
            print(f"Error initializing assistant: {e}")
            self.assistant_id = None

    async def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from the vector store based on the query.
        """
        # Generate embedding for the query using OpenAI
        response = self.openai_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"  # Or another appropriate embedding model
        )
        query_embedding = response.data[0].embedding

        # Perform a vector search in Qdrant using the generated embedding
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )

        # Extract relevant information from the search results
        contexts = []
        for point in search_result:
            context = {
                "content": point.payload.get("content", ""),
                "title": point.payload.get("title", ""),
                "source": point.payload.get("source", ""),
                "score": point.score
            }
            contexts.append(context)

        return contexts

    def format_context_for_prompt(self, contexts: List[Dict[str, Any]]) -> str:
        """
        Format the retrieved contexts into a string suitable for the LLM prompt.
        """
        formatted_contexts = []
        current_length = 0

        for context in contexts:
            context_str = f"Title: {context['title']}\nContent: {context['content']}\nSource: {context['source']}\n\n"
            # Check if adding this context would exceed the max length
            if current_length + len(context_str) > MAX_CONTEXT_LENGTH:
                break
            formatted_contexts.append(context_str)
            current_length += len(context_str)

        return "".join(formatted_contexts)

    async def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using OpenAI's Assistant API with the provided context.
        """
        if not self.assistant_id:
            raise Exception("Assistant not initialized properly")

        # Create a thread for this interaction
        thread = self.openai_client.beta.threads.create()

        # Add the user's message to the thread, including the context
        user_prompt = f"Context:\n{context}\n\nQuestion: {query}"
        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )

        # Run the assistant on the thread
        run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
            # Optionally, you can override the assistant's instructions here
        )

        # Wait for the run to complete (in a real app, you'd likely want to make this non-blocking)
        import time
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)  # Wait for 0.5 seconds before checking again
            run = self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Retrieve the messages added by the assistant to the thread
        messages = self.openai_client.beta.threads.messages.list(
            thread_id=thread.id,
            order="asc"  # Ascending order to get messages in chronological order
        )

        # Extract the assistant's response (the last message should be from the assistant)
        assistant_response = ""
        for message in reversed(messages.data):
            if message.role == "assistant":
                assistant_response = message.content[0].text.value
                break

        # Clean up: Delete the thread (optional, but good for cost management)
        # Note: We don't delete the assistant since we're reusing it
        self.openai_client.beta.threads.delete(thread.id)

        return assistant_response

    async def query(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Main method to perform RAG query: retrieve context and generate response.
        """
        # Retrieve relevant contexts
        contexts = await self.retrieve_context(user_query, top_k)

        # Format contexts for the prompt
        formatted_context = self.format_context_for_prompt(contexts)

        # Generate response
        response = await self.generate_response(user_query, formatted_context)

        return {
            "response": response,
            "contexts": contexts
        }

# Global instance of the RAG pipeline
rag_pipeline = RAGPipeline()