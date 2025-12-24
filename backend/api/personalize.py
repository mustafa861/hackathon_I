from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.auth_service import validate_token
from backend.services.skill_runner import SkillRunner
from backend.models.user import User
from backend.models.skill_request import PersonalizeRequest, PersonalizeResponse

router = APIRouter(prefix="/api", tags=["personalization"])

@router.post("/personalize", response_model=PersonalizeResponse)
def personalize_chapter(
    request: PersonalizeRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    # Check if user is authenticated
    profile = {
        "python_knowledge": False,  # Default for guests
        "has_nvidia_gpu": False,    # Default for guests
        "experience_level": "beginner"  # Default for guests
    }

    if authorization:
        # User is authenticated, get their profile
        token = authorization.replace("Bearer ", "")
        payload = validate_token(token)
        if payload:
            user_id = int(payload["sub"])
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                profile = {
                    "python_knowledge": user.python_knowledge,
                    "has_nvidia_gpu": user.has_nvidia_gpu,
                    "experience_level": user.experience_level.value
                }

    # Invoke personalizer skill
    try:
        personalized = SkillRunner.run_personalizer(request.content, profile)
        return {
            "personalized_content": personalized,
            "chapter_slug": request.chapter_slug
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))