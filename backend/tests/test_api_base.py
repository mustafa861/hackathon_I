"""
Base configuration and utilities for API integration tests.
"""

from fastapi.testclient import TestClient
from unittest.mock import patch
from ..app.main import app
from ..app.core.auth import get_current_active_user
from ..app.models.user import UserDB

# Create a TestClient for the app
client = TestClient(app)

# Mock user for testing authenticated endpoints
mock_user = UserDB(
    id=1,
    username="testuser",
    email="test@example.com",
    hashed_password="hashed_password",
    software_hardware_background="Software engineer with Python experience"
)

def get_auth_headers():
    """Helper function to get authorization headers for testing."""
    # In real tests, we would use a proper JWT token, but for testing purposes
    # we'll mock the authentication dependency
    return {"Authorization": "Bearer test_token"}

def override_auth_dependency():
    """Override the authentication dependency for testing."""
    app.dependency_overrides[get_current_active_user] = lambda: mock_user

def remove_auth_override():
    """Remove the authentication dependency override."""
    app.dependency_overrides.clear()