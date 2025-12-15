"""
API endpoints for the RAG chatbot.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..core.rag import rag_pipeline

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

# Request model
class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5  # Number of context results to retrieve

# Response model
class ChatResponse(BaseModel):
    response: str
    contexts: list

@router.post("/query", response_model=ChatResponse)
async def chatbot_query(request: ChatRequest):
    """
    Endpoint to handle chatbot queries using the RAG pipeline.
    """
    try:
        # Use the RAG pipeline to get the response
        result = await rag_pipeline.query(request.query, request.top_k)

        return ChatResponse(
            response=result["response"],
            contexts=result["contexts"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chatbot query: {str(e)}")

# Health check endpoint
@router.get("/health")
async def chatbot_health():
    """
    Health check endpoint for the chatbot API.
    """
    return {"status": "healthy", "message": "Chatbot API is running"}