from fastapi import APIRouter, Depends, HTTPException, Header
from backend.services.auth_service import validate_token
from backend.services.skill_runner import SkillRunner
from backend.models.skill_request import TranslateRequest, TranslateResponse

router = APIRouter(prefix="/api", tags=["translation"])

@router.post("/translate", response_model=TranslateResponse)
def translate_chapter(
    request: TranslateRequest,
    authorization: str = Header(...)
):
    # Validate token
    token = authorization.replace("Bearer ", "")
    payload = validate_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Invoke translator skill
    try:
        translated = SkillRunner.run_translator(request.content)
        return {
            "translated_content": translated,
            "chapter_slug": request.chapter_slug
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))