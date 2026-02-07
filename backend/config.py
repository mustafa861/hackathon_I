import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend and project root so keys work from either file
_backend_dir = Path(__file__).resolve().parent
load_dotenv(_backend_dir / ".env")
load_dotenv(_backend_dir.parent / ".env")  # project root .env
load_dotenv(".env")  # cwd .env override

def _env(key: str, default: str = None):
    """Get env var stripped of quotes and whitespace (avoids invalid keys from .env formatting)."""
    v = os.getenv(key) or default
    if v is None:
        return None
    v = v.strip().strip('"').strip("'")
    return v if v else None

DATABASE_URL = _env("DATABASE_URL")
# Default to local Qdrant for development; set QDRANT_URL in .env for Qdrant Cloud
QDRANT_URL = _env("QDRANT_URL") or "http://localhost:6333"
QDRANT_API_KEY = _env("QDRANT_API_KEY")  # Optional for local Qdrant
# API key for LLM: Gemini (preferred) or Groq
GEMINI_API_KEY = _env("GEMINI_API_KEY")
GEMINI_MODEL = _env("GEMINI_MODEL") or "gemini-2.0-flash"  # Override if a different model is needed
GROQ_API_KEY = _env("OPENAI_API_KEY")  # Groq API key (optional if using Gemini)
# API key for embeddings provider (Cohere in this implementation)
COHERE_API_KEY = _env("COHERE_API_KEY")  # This holds the Cohere API key
JWT_SECRET_KEY = _env("JWT_SECRET_KEY")

# Prefer Gemini if set, else Groq (for backward compatibility)
API_KEY = GROQ_API_KEY  # Used when Groq is selected
LLM_PROVIDER = "gemini" if GEMINI_API_KEY else "groq"
if API_KEY and not GEMINI_API_KEY:
    os.environ['API_KEY'] = API_KEY

# Provide default values to prevent None values
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing if no PostgreSQL URL provided