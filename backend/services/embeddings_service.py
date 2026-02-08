from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import cohere
from config import QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY

COLLECTION_NAME = "textbook_chapters"

# api_key is optional (e.g. for local Qdrant); only pass if set
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)

def get_cohere_client():
    """Get Cohere client for embeddings, initializing it only when needed"""
    co = cohere.Client(api_key=COHERE_API_KEY)
    return co

def setup_collection():
    """Create Qdrant collection if not exists"""
    collections = client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)  # Updated for Cohere embeddings
        )

def embed_text(text: str) -> list[float]:
    """Generate embedding using Cohere's embedding model"""
    try:
        if not COHERE_API_KEY:
            return [0.0] * 1024
        co = cohere.Client(api_key=COHERE_API_KEY)
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",  # Using Cohere's embedding model
            input_type="search_document"  # Specify the input type for document embeddings
        )
        return response.embeddings[0]  # Return the first (and only) embedding
    except Exception as e:
        # Cohere API failed or SDK version mismatch (e.g. CohereError moved); use default embedding
        print(f"Embedding error: {str(e)}")
        return [0.0] * 1024  # Default embedding vector size for Cohere's model

def add_textbook_content(text: str, chapter_slug: str = "", section_title: str = ""):
    """Add textbook content to the vector database"""
    try:
        # Generate embedding for the text
        vector = embed_text(text)

        # Create a unique ID for this content (using a simple counter approach)
        import uuid
        point_id = str(uuid.uuid4())

        # Prepare the payload with metadata
        payload = {
            "text": text,
            "chapter_slug": chapter_slug,
            "section_title": section_title
        }

        # Upsert the point to the collection
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        return True
    except Exception as e:
        print(f"Error adding textbook content: {str(e)}")
        return False


def search_similar(query: str, limit: int = 5) -> list:
    """Search for similar chapter sections"""
    query_vector = embed_text(query)
    # Use query_points (current API); older clients had .search()
    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
        )
        results = getattr(response, "points", None) or getattr(response, "result", []) or []
        results = list(results)
    else:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
        )
    return results