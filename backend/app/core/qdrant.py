"""
Qdrant Cloud client configuration.
"""

import os
from qdrant_client import QdrantClient

# Get Qdrant URL and API key from environment variables
QDRANT_URL = os.getenv("QDRANT_URL", "https://af6b048c-3bcb-4af3-b2fa-5a4f50eec6fb.us-east4-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.aP2xr5n4clzNneNSDO45LED1uWQvD1wIm4m4dyBAU6A")

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    # timeout=10  # Optional: Set a timeout for requests
)

def get_qdrant_client():
    """Function to get the configured Qdrant client instance."""
    return client