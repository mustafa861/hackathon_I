from fastapi import APIRouter, Depends, HTTPException, Header
from services.embeddings_service import search_similar
from services.auth_service import validate_token
from services.llm_service import complete as llm_complete
from models.chat_schemas import ChatRequest, ChatResponse
from config import GEMINI_API_KEY, API_KEY, LLM_PROVIDER

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

        system = "You are a robotics tutor. Answer questions based on the provided textbook context. Cite sections using format 'See Chapter X.Y: Title'."
        user_content = f"Context:\n{context}\n\nQuestion: {request.query}\n\nSelected text: {request.selected_context}"
        answer = llm_complete(system, user_content, temperature=0.7, max_tokens=1000)

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

    except Exception as e:
        # Handle any other errors
        import traceback
        print(f"Chat error: {str(e)}")
        traceback.print_exc()
        err_upper = str(e).upper()
        # When Qdrant is down, fall back to answering without textbook context
        if "QDRANT" in err_upper or "CONNECTION" in err_upper or "HOST" in err_upper or "REFUSED" in err_upper:
            try:
                system = "You are a robotics tutor. Answer the user's question using general knowledge. Say you don't have the textbook in front of you, so this is a general answer."
                answer = llm_complete(system, request.query, temperature=0.7, max_tokens=1000)
                return {"answer": answer, "sources": []}
            except Exception as fallback_err:
                print(f"Fallback LLM error: {fallback_err}")
                traceback.print_exc()
                fallback_upper = str(fallback_err).upper()
                if "429" in fallback_upper or "QUOTA" in fallback_upper:
                    hint = "Gemini quota exceeded. Add OPENAI_API_KEY (Groq) to backend/.env to use Groq as fallback (free key at console.groq.com), or check usage at aistudio.google.com."
                elif LLM_PROVIDER == "groq" or not GEMINI_API_KEY:
                    hint = "Add GEMINI_API_KEY=your-key to backend/.env (get one at aistudio.google.com/apikey)."
                else:
                    hint = "Check that GEMINI_API_KEY in backend/.env is valid. Restart the backend after editing .env."
                return {
                    "answer": f"Chat couldn't reach the AI: {hint}",
                    "sources": []
                }
        elif "429" in err_upper or "QUOTA" in err_upper:
            return {
                "answer": "Gemini quota exceeded. Add OPENAI_API_KEY (Groq) to backend/.env to use Groq as fallback (free key at console.groq.com), or check usage at aistudio.google.com.",
                "sources": []
            }
        elif "GROQ FALLBACK FAILED" in err_upper:
            return {
                "answer": "Gemini quota exceeded and Groq fallback failed. Check that OPENAI_API_KEY in backend/.env is a valid Groq API key (get one at console.groq.com), then restart the backend.",
                "sources": []
            }
        elif "API_KEY" in err_upper or "AUTH" in err_upper or "AUTHENTICATION" in err_upper:
            return {
                "answer": "I'm unable to process your request due to API configuration issues. Set GEMINI_API_KEY or OPENAI_API_KEY (Groq) in backend/.env.",
                "sources": []
            }
        elif "404" in err_upper or "NOT FOUND" in err_upper or "PAGE NOT FOUND" in err_upper:
            return {
                "answer": "A service returned 'not found' (404). Check that QDRANT_URL in backend/.env points to your Qdrant instance, and that the backend is running. Use POST /chat to send messages.",
                "sources": []
            }
        else:
            return {
                "answer": f"Sorry, I encountered an error while processing your request: {str(e)}",
                "sources": []
            }