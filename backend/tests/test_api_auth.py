"""
Integration tests for the authentication API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ..app.main import app  # Assuming you have a main.py that creates the FastAPI app
from ..app.core.database import Base, get_db
from ..app.api.auth import router as auth_router
from ..app.api.chatbot import router as chatbot_router
from ..app.api.personalization import router as personalization_router
from ..app.api.translation import router as translation_router

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Create a TestClient for the app
client = TestClient(app)

def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the get_db dependency in the app
app.dependency_overrides[get_db] = override_get_db

def test_signup_new_user():
    """Test signing up a new user."""
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "software_hardware_background": "Software engineer"
    }

    response = client.post("/auth/signup", json=signup_data)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["software_hardware_background"] == "Software engineer"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_signup_duplicate_user():
    """Test signing up with duplicate username/email."""
    # First, sign up a user
    signup_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123",
        "software_hardware_background": "Software engineer"
    }
    client.post("/auth/signup", json=signup_data)

    # Try to sign up with the same username
    duplicate_data = {
        "username": "testuser2",
        "email": "different@example.com",
        "password": "testpassword123",
        "software_hardware_background": "Software engineer"
    }
    response = client.post("/auth/signup", json=duplicate_data)
    assert response.status_code == 400

    # Try to sign up with the same email
    duplicate_data = {
        "username": "differentuser",
        "email": "test2@example.com",
        "password": "testpassword123",
        "software_hardware_background": "Software engineer"
    }
    response = client.post("/auth/signup", json=duplicate_data)
    assert response.status_code == 400

def test_signin_valid_user():
    """Test signing in with valid credentials."""
    # First, create a user
    signup_data = {
        "username": "signin_test",
        "email": "signin@example.com",
        "password": "testpassword123",
        "software_hardware_background": "Software engineer"
    }
    client.post("/auth/signup", json=signup_data)

    # Now try to sign in
    signin_data = {
        "username": "signin_test",
        "password": "testpassword123"
    }
    response = client.post("/auth/signin", json=signin_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_signin_invalid_credentials():
    """Test signing in with invalid credentials."""
    signin_data = {
        "username": "nonexistent_user",
        "password": "wrongpassword"
    }
    response = client.post("/auth/signin", json=signin_data)
    assert response.status_code == 401

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/auth/health")
    assert response.status_code == 200