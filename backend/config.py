import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')  # Explicitly specify the .env file path

DATABASE_URL = os.getenv("DATABASE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# API key for LLM provider (Groq in this implementation)
GROQ_API_KEY = os.getenv("OPENAI_API_KEY")  # This holds the Groq API key
# API key for embeddings provider (Cohere in this implementation)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # This holds the Cohere API key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Also set API_KEY for backward compatibility with services that still reference it
API_KEY = GROQ_API_KEY  # For backward compatibility
if API_KEY:
    os.environ['API_KEY'] = API_KEY

# Provide default values to prevent None values
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing if no PostgreSQL URL provided