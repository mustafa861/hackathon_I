"""
Unit tests for the RAG (Retrieval-Augmented Generation) module.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from ..app.core.rag import RAGPipeline

@pytest.mark.asyncio
async def test_rag_pipeline_initialization():
    """Test that the RAG pipeline initializes correctly."""
    with patch('..app.core.rag.get_qdrant_client'), \
         patch('..app.core.rag.OpenAI'):
        rag = RAGPipeline()

        assert rag.collection_name == "book_content_embeddings"
        assert rag.openai_client is not None
        assert rag.qdrant_client is not None

@pytest.mark.asyncio
async def test_format_context_for_prompt():
    """Test the context formatting function."""
    with patch('..app.core.rag.get_qdrant_client'), \
         patch('..app.core.rag.OpenAI'):
        rag = RAGPipeline()

        contexts = [
            {"content": "Content 1", "title": "Title 1", "source": "Source 1", "score": 0.9},
            {"content": "Content 2", "title": "Title 2", "source": "Source 2", "score": 0.8}
        ]

        formatted = rag.format_context_for_prompt(contexts)

        # Check that the formatted string contains the expected content
        assert "Title: Title 1" in formatted
        assert "Content: Content 1" in formatted
        assert "Source: Source 1" in formatted
        assert "Title: Title 2" in formatted
        assert "Content: Content 2" in formatted

@pytest.mark.asyncio
async def test_format_context_for_prompt_length_limit():
    """Test that the context formatting respects the length limit."""
    with patch('..app.core.rag.get_qdrant_client'), \
         patch('..app.core.rag.OpenAI'):
        rag = RAGPipeline()

        # Create contexts that exceed the length limit
        long_content = "A" * 2500  # This should exceed the default limit
        contexts = [
            {"content": "Short content", "title": "Title 1", "source": "Source 1", "score": 0.9},
            {"content": long_content, "title": "Title 2", "source": "Source 2", "score": 0.8}
        ]

        formatted = rag.format_context_for_prompt(contexts)

        # The long content should be excluded due to length limit
        assert "Short content" in formatted
        # The total length should be within the limit
        assert len(formatted) <= 2000  # MAX_CONTEXT_LENGTH

@pytest.mark.asyncio
async def test_rag_pipeline_query():
    """Test the full RAG pipeline query function."""
    with patch('..app.core.rag.get_qdrant_client') as mock_qdrant, \
         patch('..app.core.rag.OpenAI') as mock_openai:

        # Mock Qdrant client
        mock_qdrant_instance = AsyncMock()
        mock_search_result = [
            MagicMock(payload={"content": "Test content", "title": "Test Title", "source": "Test Source"}, score=0.9)
        ]
        mock_qdrant_instance.search.return_value = mock_search_result
        mock_qdrant.return_value = mock_qdrant_instance

        # Mock OpenAI client
        mock_openai_instance = MagicMock()
        mock_assistant = MagicMock()
        mock_assistant.id = "test_assistant_id"
        mock_openai_instance.beta.assistants.create.return_value = mock_assistant

        # Mock thread creation
        mock_thread = MagicMock()
        mock_thread.id = "test_thread_id"
        mock_openai_instance.beta.threads.create.return_value = mock_thread

        # Mock message creation
        mock_message = MagicMock()
        mock_openai_instance.beta.threads.messages.create.return_value = mock_message

        # Mock run creation
        mock_run = MagicMock()
        mock_run.id = "test_run_id"
        mock_run.status = "completed"
        mock_openai_instance.beta.threads.runs.create.return_value = mock_run
        mock_openai_instance.beta.threads.runs.retrieve.return_value = mock_run

        # Mock message listing
        mock_response_message = MagicMock()
        mock_response_message.role = "assistant"
        mock_response_message.content = [MagicMock(text=MagicMock(value="Test response"))]
        mock_messages = MagicMock()
        mock_messages.data = [mock_response_message]
        mock_openai_instance.beta.threads.messages.list.return_value = mock_messages

        mock_openai.return_value = mock_openai_instance

        rag = RAGPipeline()

        result = await rag.query("Test query")

        # Verify the result structure
        assert "response" in result
        assert "contexts" in result
        assert result["response"] == "Test response"
        assert len(result["contexts"]) == 1
        assert result["contexts"][0]["content"] == "Test content"