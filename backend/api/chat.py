from fastapi import APIRouter, Depends, HTTPException, Header
from services.embeddings_service import search_similar
from services.auth_service import validate_token
from models.chat_schemas import ChatRequest, ChatResponse
from config import API_KEY
import google.generativeai as genai
import google.api_core.exceptions

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_textbook(
    request: ChatRequest,
    authorization: str = Header(None)
):
    # Authentication is optional - check if user is authenticated
    # For guest access, we allow chat without authentication
    if authorization:
        # User is authenticated, validate token
        token = authorization.replace("Bearer ", "")
        payload = validate_token(token)
        if not payload:
            # If token is invalid, proceed as guest
            pass

    try:
        # Search Qdrant for relevant sections
        results = search_similar(request.query + " " + request.selected_context, limit=3)

        # Build context from results
        context_parts = [r.payload.get("text", "") for r in results]
        context = "\n\n".join(context_parts)

        # Generate answer with Google's Generative AI
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""Context:\n{context}\n\nQuestion: {request.query}\n\nSelected text: {request.selected_context}

        You are a robotics tutor. Answer questions based on the provided textbook context. Cite sections using format 'See Chapter X.Y: Title'."""

        response = model.generate_content(prompt)
        answer = response.text if response.text else "I couldn't generate a response for your question."

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

    except google.api_core.exceptions.ResourceExhausted:
        # Handle quota exceeded error
        return {
            "answer": "I'm currently unable to process your request due to API quota limits. Please try again later.",
            "sources": []
        }
    except Exception as e:
        # Handle any other errors
        print(f"Chat error: {str(e)}")  # Log the error
        return {
            "answer": "Sorry, I encountered an error while processing your request. Please try again.",
            "sources": []
        }