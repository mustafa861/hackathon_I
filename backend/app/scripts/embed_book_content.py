"""
Script to initialize Qdrant collection for book content embeddings
and potentially process existing book content.
"""

import os
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..core.qdrant import get_qdrant_client

# Configuration
COLLECTION_NAME = "book_content_embeddings"
VECTOR_SIZE = 1536  # Default size for OpenAI embeddings (text-embedding-ada-002)

async def initialize_qdrant_collection():
    """
    Initialize the Qdrant collection for storing book content embeddings.
    """
    client = get_qdrant_client()

    # Check if collection already exists
    collection_exists = False
    try:
        await client.get_collection(COLLECTION_NAME)
        collection_exists = True
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Collection '{COLLECTION_NAME}' does not exist. Creating it...")

    if not collection_exists:
        # Create the collection
        await client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")

    # Optionally, configure payload indexes here if needed
    # await client.create_payload_index(
    #     collection_name=COLLECTION_NAME,
    #     field_name="book_id",
    #     field_schema=models.PayloadSchemaType.KEYWORD,
    # )

async def main():
    """
    Main function to run the initialization.
    """
    print("Initializing Qdrant collection for book content embeddings...")
    await initialize_qdrant_collection()
    print("Initialization complete.")

if __name__ == "__main__":
    asyncio.run(main())