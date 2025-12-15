"""
Integration tests for the chatbot API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from ..app.main import app  # Assuming you have a main.py that creates the FastAPI app

client = TestClient(app)

def test_chatbot_query():
    """Test the chatbot query endpoint."""
    # Mock the RAG pipeline to avoid calling external APIs during testing
    with patch('..app.api.chatbot.rag_pipeline') as mock_rag:
        mock_result = AsyncMock()
        mock_result.return_value = {
            "response": "Test response from chatbot",
            "contexts": [
                {"content": "Test context", "title": "Test Title", "source": "Test Source", "score": 0.9}
            ]
        }
        mock_rag.query = mock_result

        query_data = {
            "query": "What is humanoid robotics?",
            "top_k": 3
        }

        response = client.post("/chatbot/query", json=query_data)
        assert response.status_code == 200

        data = response.json()
        assert data["response"] == "Test response from chatbot"
        assert len(data["contexts"]) == 1
        assert data["contexts"][0]["content"] == "Test context"

def test_chatbot_query_missing_query():
    """Test the chatbot query endpoint with missing query."""
    query_data = {
        "top_k": 3
    }

    response = client.post("/chatbot/query", json=query_data)
    # Should return 422 for validation error since query is required
    assert response.status_code == 422

def test_chatbot_health():
    """Test the chatbot health check endpoint."""
    response = client.get("/chatbot/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data