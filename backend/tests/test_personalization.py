"""
Unit tests for the personalization module.
"""

import pytest
from unittest.mock import patch, AsyncMock
from ..app.core.personalization import personalize_content

@pytest.mark.asyncio
async def test_personalize_content_with_background():
    """Test that content is personalized based on user background."""
    original_content = "This is a technical explanation about robotics."
    user_background = "software engineer with experience in Python and AI"

    with patch('..app.core.personalization.openai_client') as mock_openai:
        mock_response = AsyncMock()
        mock_response.choices = [type('obj', (object,), {
            'message': type('obj', (object,), {'content': 'Personalized content for software engineers...'})
        })()]

        mock_openai.chat.completions.create.return_value = mock_response

        result = await personalize_content(
            content=original_content,
            user_background=user_background
        )

        # Verify the result is the mocked response
        assert result == "Personalized content for software engineers..."

@pytest.mark.asyncio
async def test_personalize_content_without_background():
    """Test that content is returned unchanged when no background is provided."""
    original_content = "This is a technical explanation about robotics."

    result = await personalize_content(
        content=original_content,
        user_background=None
    )

    # Should return the original content when no background is provided
    assert result == original_content

@pytest.mark.asyncio
async def test_personalize_content_empty_background():
    """Test that content is returned unchanged when background is empty."""
    original_content = "This is a technical explanation about robotics."

    result = await personalize_content(
        content=original_content,
        user_background=""
    )

    # Should return the original content when background is empty
    assert result == original_content

@pytest.mark.asyncio
async def test_personalize_content_error_handling():
    """Test that original content is returned when personalization fails."""
    original_content = "This is a technical explanation about robotics."
    user_background = "software engineer"

    with patch('..app.core.personalization.openai_client') as mock_openai:
        # Simulate an API error
        mock_openai.chat.completions.create.side_effect = Exception("API Error")

        result = await personalize_content(
            content=original_content,
            user_background=user_background
        )

        # Should return the original content when an error occurs
        assert result == original_content