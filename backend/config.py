import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')  # Explicitly specify the .env file path

DATABASE_URL = os.getenv("DATABASE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# Use the same variable name but it can be either OpenAI or Google API key
API_KEY = os.getenv("OPENAI_API_KEY")  # This will hold the Google API key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Provide default values to prevent None values
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing if no PostgreSQL URL provided