"""
Integration tests for the personalization API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from ..app.main import app  # Assuming you have a main.py that creates the FastAPI app

client = TestClient(app)

def test_personalization_health():
    """Test the personalization health check endpoint."""
    response = client.get("/personalization/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data