"""
API endpoints for content translation.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..models.user import UserDB
from ..core.auth import get_current_active_user
from ..core.translation import translate_to_urdu

router = APIRouter(prefix="/translation", tags=["translation"])

# Request/Response models
class TranslateContentRequest(BaseModel):
    content: str
    target_language: str = "ur"  # Default to Urdu
    chapter_id: Optional[str] = None
    section_id: Optional[str] = None

class TranslateContentResponse(BaseModel):
    translated_content: str

@router.post("/translate", response_model=TranslateContentResponse)
async def translate_content_endpoint(
    request: TranslateContentRequest,
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Translate content to the specified language (default Urdu).
    """
    if request.target_language.lower() != "ur":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Urdu translation is currently supported"
        )

    # Use the translation logic to translate the content
    translated_content = await translate_to_urdu(
        content=request.content,
        chapter_id=request.chapter_id,
        section_id=request.section_id
    )

    return TranslateContentResponse(translated_content=translated_content)

# Health check endpoint
@router.get("/health")
async def translation_health():
    """
    Health check endpoint for the translation API.
    """
    return {"status": "healthy", "message": "Translation API is running"}