from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import google.generativeai as genai
from config import QDRANT_URL, QDRANT_API_KEY, API_KEY

COLLECTION_NAME = "textbook_chapters"

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_google_client():
    """Get Google Generative AI client, initializing it only when needed"""
    genai.configure(api_key=API_KEY)  # Using the new unified API key variable
    return genai

def setup_collection():
    """Create Qdrant collection if not exists"""
    collections = client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

def embed_text(text: str) -> list[float]:
    """Generate embedding using Google's embedding model"""
    genai.configure(api_key=API_KEY)  # Using the new unified API key variable
    model = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return model['embedding']

def search_similar(query: str, limit: int = 5) -> list:
    """Search for similar chapter sections"""
    query_vector = embed_text(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )
    return results