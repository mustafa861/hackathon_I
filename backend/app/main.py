"""
Main entry point for the FastAPI application.
"""

from fastapi import FastAPI
from .api.chatbot import router as chatbot_router
from .api.auth import router as auth_router
from .api.personalization import router as personalization_router
from .api.translation import router as translation_router

app = FastAPI(title="Physical AI & Humanoid Robotics API")

# Include API routers
app.include_router(chatbot_router)
app.include_router(auth_router)
app.include_router(personalization_router)
app.include_router(translation_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)