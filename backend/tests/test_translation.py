"""
Unit tests for the translation module.
"""

import pytest
from unittest.mock import patch, AsyncMock
from ..app.core.translation import translate_to_urdu

@pytest.mark.asyncio
async def test_translate_to_urdu():
    """Test that content is translated to Urdu."""
    original_content = "This is a technical explanation about robotics."

    with patch('..app.core.translation.openai_client') as mock_openai:
        mock_response = AsyncMock()
        mock_response.choices = [type('obj', (object,), {
            'message': type('obj', (object,), {'content': 'روبوٹکس کے بارے میں ایک تکنیکی وضاحت ہے۔'})
        })()]

        mock_openai.chat.completions.create.return_value = mock_response

        result = await translate_to_urdu(content=original_content)

        # Verify the result is the mocked Urdu translation
        assert result == "روبوٹکس کے بارے میں ایک تکنیکی وضاحت ہے۔"

@pytest.mark.asyncio
async def test_translate_to_urdu_error_handling():
    """Test that original content is returned when translation fails."""
    original_content = "This is a technical explanation about robotics."

    with patch('..app.core.translation.openai_client') as mock_openai:
        # Simulate an API error
        mock_openai.chat.completions.create.side_effect = Exception("API Error")

        result = await translate_to_urdu(content=original_content)

        # Should return the original content when an error occurs
        assert result == original_content

@pytest.mark.asyncio
async def test_translate_empty_content():
    """Test translation behavior with empty content."""
    with patch('..app.core.translation.openai_client') as mock_openai:
        mock_response = AsyncMock()
        mock_response.choices = [type('obj', (object,), {
            'message': type('obj', (object,), {'content': ''})
        })()]

        mock_openai.chat.completions.create.return_value = mock_response

        result = await translate_to_urdu(content="")

        # Result would be empty as well
        assert result == ""