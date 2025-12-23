from fastapi import APIRouter, Depends, HTTPException, Header
from backend.services.embeddings_service import search_similar
from backend.services.auth_service import validate_token
from backend.models.chat_schemas import ChatRequest, ChatResponse
from backend.config import API_KEY
import google.generativeai as genai

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_textbook(
    request: ChatRequest,
    authorization: str = Header(...)
):
    # Validate token
    token = authorization.replace("Bearer ", "")
    payload = validate_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Search Qdrant for relevant sections
    results = search_similar(request.query + " " + request.selected_context, limit=3)

    # Build context from results
    context_parts = [r.payload.get("text", "") for r in results]
    context = "\n\n".join(context_parts)

    # Generate answer with Google's Generative AI
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Context:\n{context}\n\nQuestion: {request.query}\n\nSelected text: {request.selected_context}

    You are a robotics tutor. Answer questions based on the provided textbook context. Cite sections using format 'See Chapter X.Y: Title'."""

    response = model.generate_content(prompt)
    answer = response.text

    # Extract sources
    sources = [
        {
            "chapter": r.payload.get("chapter_slug", ""),
            "section": r.payload.get("section_title", ""),
            "url": f"/docs/{r.payload.get('chapter_slug', '')}"
        }
        for r in results
    ]

    return {"answer": answer, "sources": sources}