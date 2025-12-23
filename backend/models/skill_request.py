from pydantic import BaseModel

class PersonalizeRequest(BaseModel):
    chapter_slug: str
    content: str

class PersonalizeResponse(BaseModel):
    personalized_content: str
    chapter_slug: str

class TranslateRequest(BaseModel):
    chapter_slug: str
    content: str

class TranslateResponse(BaseModel):
    translated_content: str
    chapter_slug: str