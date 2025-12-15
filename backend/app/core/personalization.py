"""
Content personalization logic for the application.
"""

import re
from typing import Optional
from openai import OpenAI
import os

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def personalize_content(
    content: str,
    user_background: Optional[str] = None,
    chapter_id: Optional[str] = None,
    section_id: Optional[str] = None
) -> str:
    """
    Personalize content based on the user's software/hardware background.

    This function uses AI to adapt the content to the user's background.
    """
    if not user_background:
        # If no user background is provided, return the original content
        return content

    # Create a prompt for the AI model to personalize the content
    system_prompt = (
        "You are an expert in Physical AI & Humanoid Robotics education. "
        "Your task is to personalize educational content based on the user's background. "
        "Modify the content to be more relevant and understandable for the user, "
        "using examples and explanations that align with their expertise. "
        "Preserve the core information and meaning of the original text, "
        "but adapt the language, examples, and focus to match the user's background. "
        "If the user's background is more software-focused, emphasize software aspects. "
        "If more hardware-focused, emphasize hardware aspects. "
        "For mixed backgrounds, provide a balanced perspective. "
        "For beginners, add more explanations. For experts, add more technical depth."
    )

    user_prompt = (
        f"User Background: {user_background}\n\n"
        f"Original Content: {content}\n\n"
        f"Please provide a personalized version of the content that is tailored to the user's background."
    )

    try:
        # Use OpenAI API to generate personalized content
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or another appropriate model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000,  # Adjust as needed
            temperature=0.7
        )

        personalized_content = response.choices[0].message.content
        return personalized_content

    except Exception as e:
        # If personalization fails, return the original content
        print(f"Personalization failed: {e}")
        return content

def get_content_for_personalization(content: str, section_id: Optional[str] = None) -> str:
    """
    Extract specific section from content if section_id is provided,
    otherwise return the full content.
    """
    if section_id:
        # This is a simplified approach - in a real implementation,
        # you might have more sophisticated section identification
        # For now, we'll return the full content and let the AI handle section-specific personalization
        return content
    return content