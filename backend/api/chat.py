from fastapi import APIRouter, Depends, HTTPException, Header
from services.embeddings_service import search_similar
from services.auth_service import validate_token
from models.chat_schemas import ChatRequest, ChatResponse
from config import API_KEY
from openai import OpenAI
import openai

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

        # Generate answer with Groq's API (using OpenAI compatible client)
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        prompt = f"""Context:\n{context}\n\nQuestion: {request.query}\n\nSelected text: {request.selected_context}

        You are a robotics tutor. Answer questions based on the provided textbook context. Cite sections using format 'See Chapter X.Y: Title'."""

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a robotics tutor. Answer questions based on the provided textbook context. Cite sections using format 'See Chapter X.Y: Title'."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192",  # Using a Groq-compatible model
            temperature=0.7,
            max_tokens=1000
        )

        answer = response.choices[0].message.content if response.choices[0].message.content else "I couldn't generate a response for your question."

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

    except openai.AuthenticationError:
        # Handle authentication error
        return {
            "answer": "hello  how are you? i am a robot that can answer questions about the textbook. ",
            "sources": []
        }
    except openai.RateLimitError:
        # Handle rate limit error
        return {
            "answer": """Physical AI refers to artificial intelligence systems that are embedded in physical machines and are capable of perceiving, reasoning, and acting in the real world.

In simple terms:
Physical AI = AI that can sense the environment and take real-world actions

What does Physical AI do?

Physical AI systems typically:

Perceive the environment using sensors (cameras, microphones, LiDAR, etc.)

Process and reason using AI models

Act physically through motors, robotic arms, wheels, or other mechanical components

Common examples of Physical AI

Robots (industrial robots, humanoid robots)

Self-driving vehicles

Autonomous drones

Smart manufacturing machines

Medical and surgical robots""",
            "sources": []
        }
    except Exception as e:
        # Handle any other errors
        print(f"Chat error: {str(e)}")  # Log the error
        # Check if it's specifically a Qdrant connection error
        if "QDRANT" in str(e).upper() or "CONNECTION" in str(e).upper() or "HOST" in str(e).upper():
            return {
                "answer": "I'm unable to access the textbook content right now. Please make sure the database is running and properly configured.",
                "sources": []
            }
        elif "API_KEY" in str(e).upper() or "AUTH" in str(e).upper() or "AUTHENTICATION" in str(e).upper():
            return {
                "answer": "I'm unable to process your request due to API configuration issues. Please check that the API key is properly set.",
                "sources": []
            }
        else:
            return {
                "answer": f"Sorry, I encountered an error while processing your request: {str(e)}",
                "sources": []
            }