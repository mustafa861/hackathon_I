from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, chat, personalize, translate
from database import Base, engine
from services.embeddings_service import setup_collection

app = FastAPI(title="Physical AI Textbook API", version="1.0.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize Qdrant collection on startup
@app.on_event("startup")
def startup_event():
    try:
        setup_collection()
    except Exception as e:
        print(f"Warning: Could not initialize Qdrant collection: {e}")
        print("This is expected if Qdrant is not running or configured.")

# CORS (allow Docusaurus frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(personalize.router)
app.include_router(translate.router)

@app.get("/")
def root():
    return {"message": "Physical AI Textbook API", "version": "1.0.0"}

@app.get("/health")
def health():
    """Health check; use POST /chat for the chatbot."""
    return {"status": "ok"}