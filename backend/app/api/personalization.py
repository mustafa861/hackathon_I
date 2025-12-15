"""
API endpoints for content personalization.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..models.user import UserDB
from ..core.auth import get_current_active_user
from ..core.personalization import personalize_content

router = APIRouter(prefix="/personalization", tags=["personalization"])

# Request/Response models
class PersonalizeContentRequest(BaseModel):
    content: str
    chapter_id: Optional[str] = None
    section_id: Optional[str] = None

class PersonalizeContentResponse(BaseModel):
    personalized_content: str

@router.post("/personalize", response_model=PersonalizeContentResponse)
async def personalize_content_endpoint(
    request: PersonalizeContentRequest,
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Personalize content based on the user's software/hardware background.
    """
    # Use the personalization logic to adjust the content
    personalized_content = await personalize_content(
        content=request.content,
        user_background=current_user.software_hardware_background,
        chapter_id=request.chapter_id,
        section_id=request.section_id
    )

    return PersonalizeContentResponse(personalized_content=personalized_content)

# Health check endpoint
@router.get("/health")
async def personalization_health():
    """
    Health check endpoint for the personalization API.
    """
    return {"status": "healthy", "message": "Personalization API is running"}