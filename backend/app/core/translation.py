"""
Urdu translation logic for the application.
"""

import re
from typing import Optional
from openai import OpenAI
import os

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def translate_to_urdu(
    content: str,
    chapter_id: Optional[str] = None,
    section_id: Optional[str] = None
) -> str:
    """
    Translate content to Urdu.

    This function uses AI to translate the content to Urdu while preserving
    the structure and formatting.
    """
    # Create a prompt for the AI model to translate the content to Urdu
    system_prompt = (
        "You are a professional translator specializing in translating technical content from English to Urdu. "
        "Your task is to translate the provided content to Urdu while preserving the original structure, formatting, and markup. "
        "Maintain the same HTML tags, markdown formatting, and document structure. "
        "Translate the text content within tags/punctuation appropriately to Urdu. "
        "Ensure that technical terms are translated appropriately or kept in English if there's no direct Urdu equivalent. "
        "Preserve code blocks, mathematical expressions, and other special formatting exactly as they are."
    )

    user_prompt = (
        f"Please translate the following content to Urdu while preserving structure and formatting:\n\n"
        f"Content: {content}\n\n"
        f"Provide the translated content in the same format with Urdu text."
    )

    try:
        # Use OpenAI API to translate the content
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or another appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,  # Adjust as needed for longer content
            temperature=0.3  # Lower temperature for more consistent translation
        )

        translated_content = response.choices[0].message.content
        return translated_content

    except Exception as e:
        # If translation fails, return the original content
        print(f"Translation failed: {e}")
        return content