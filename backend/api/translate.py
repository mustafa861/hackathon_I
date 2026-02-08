# from fastapi import APIRouter, Depends, HTTPException, Header
# from services.auth_service import validate_token
# from services.skill_runner import SkillRunner
# from models.skill_request import TranslateRequest, TranslateResponse

# router = APIRouter(prefix="/api", tags=["translation"])

# @router.post("/translate", response_model=TranslateResponse)
# def translate_chapter(
#     request: TranslateRequest,
#     authorization: str = Header(None)
# ):
#     # Authentication is optional - check if user is authenticated
#     if authorization:
#         # User is authenticated, validate token
#         token = authorization.replace("Bearer ", "")
#         payload = validate_token(token)
#         if not payload:
#             raise HTTPException(status_code=401, detail="Invalid token")

#     # Validate the request content
#     if not request.content or len(request.content.strip()) == 0:
#         return {
#             "translated_content": "کوئی مواد ترجمہ کے لیے دستیاب نہیں ہے",  # "No content available for translation" in Urdu
#             "chapter_slug": request.chapter_slug or "unknown"
#         }

#     # Log the incoming request for debugging
#     print(f"Translating content of length: {len(request.content)} characters")

#     # Invoke translator skill
#     try:
#         translated = SkillRunner.run_translator(request.content)

#         # Ensure the translated content is valid
#         if not translated or translated.strip() == "":
#             translated = "ترجمہ مکمل نہیں کیا جا سکا"  # "Translation could not be completed" in Urdu

#         return {
#             "translated_content": translated,
#             "chapter_slug": request.chapter_slug or "unknown"
#         }
#     except RuntimeError as e:
#         # More specific error handling for translation
#         error_msg = str(e)
#         print(f"Translation runtime error: {error_msg}")
#         if "API_KEY" in error_msg.upper() or "GOOGLE" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper():
#             raise HTTPException(status_code=500, detail="Translation service is not properly configured. Please check API key settings.")
#         else:
#             raise HTTPException(status_code=500, detail=f"Translation failed: {error_msg}")
#     except Exception as e:
#         # Catch any other exceptions
#         error_msg = str(e)
#         print(f"Unexpected translation error: {error_msg}")
#         raise HTTPException(status_code=500, detail=f"Unexpected error during translation: {error_msg}")

from fastapi import APIRouter, Depends, HTTPException, Header
from services.auth_service import validate_token
from services.skill_runner import SkillRunner
from models.skill_request import TranslateRequest, TranslateResponse

router = APIRouter(prefix="/api", tags=["translation"])

@router.post("/translate", response_model=TranslateResponse)
def translate_chapter(
    request: TranslateRequest,
    authorization: str = Header(None)
):
    # Authentication is optional - check if user is authenticated
    if authorization:
        try:
            # User is authenticated, validate token
            token = authorization.replace("Bearer ", "")
            payload = validate_token(token)
            if not payload:
                # ✅ CHANGED: Don't raise error, just log and continue
                print("Invalid token provided, continuing without authentication")
        except Exception as e:
            # ✅ CHANGED: Don't raise error on token validation failure
            print(f"Token validation error: {e}, continuing without authentication")

    # Validate the request content
    if not request.content or len(request.content.strip()) == 0:
        return {
            "translated_content": "کوئی مواد ترجمہ کے لیے دستیاب نہیں ہے",  # "No content available for translation" in Urdu
            "chapter_slug": request.chapter_slug or "unknown"
        }

    # Log the incoming request for debugging
    print(f"Translating content of length: {len(request.content)} characters")

    # Invoke translator skill
    try:
        translated = SkillRunner.run_translator(request.content)

        # Ensure the translated content is valid
        if not translated or translated.strip() == "":
            translated = "ترجمہ مکمل نہیں کیا جا سکا"  # "Translation could not be completed" in Urdu

        return {
            "translated_content": translated,
            "chapter_slug": request.chapter_slug or "unknown"
        }
    except RuntimeError as e:
        # More specific error handling for translation
        error_msg = str(e)
        print(f"Translation runtime error: {error_msg}")
        if "API_KEY" in error_msg.upper() or "GOOGLE" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper():
            raise HTTPException(status_code=500, detail="Translation service is not properly configured. Please check API key settings.")
        else:
            raise HTTPException(status_code=500, detail=f"Translation failed: {error_msg}")
    except Exception as e:
        # Catch any other exceptions
        error_msg = str(e)
        print(f"Unexpected translation error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Unexpected error during translation: {error_msg}")