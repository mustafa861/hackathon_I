import json
import os
from typing import Dict
from services.llm_service import complete as llm_complete

class SkillRunner:
    """Service for invoking agent skills (uses Gemini or Groq via llm_service)"""

    @staticmethod
    def run_quiz_generator(markdown: str) -> str:
        """Generate quiz for chapter markdown using the quiz agent"""
        try:
            system = "You are an educational assistant that creates quizzes based on textbook content. Generate 5 multiple-choice questions with 4 options each and indicate the correct answer."
            user = f"Generate a quiz based on the following textbook content. Create 5 multiple-choice questions with 4 options each. Include the correct answer for each question. Format the output as clear questions with options and answers.\n\nTextbook content:\n{markdown}"
            return llm_complete(system, user, temperature=0.7, max_tokens=1500)
        except Exception as e:
            raise RuntimeError(f"Quiz generation failed: {str(e)}")

    @staticmethod
    def run_translator(markdown: str) -> str:
        """Translate markdown to Urdu using the translation agent"""
        try:
            # Check if markdown content is valid
            if not markdown or len(markdown.strip()) == 0:
                return "کوئی مواد ترجمہ کے لیے دستیاب نہیں ہے"  # "No content available for translation" in Urdu

            system = "You are a professional translator that translates English text to Urdu. Maintain accuracy and cultural appropriateness."
            user = f"Translate the following English text to Urdu. Preserve the meaning and context. Keep technical terms in English if there's no direct Urdu equivalent. Provide only the translated text in Urdu.\n\nText to translate:\n{markdown}"

            result = llm_complete(system, user, temperature=0.3, max_tokens=1500)

            # Check if the result is valid
            if not result or result.strip() in ["", "I couldn't generate a response.", "I couldn't generate a response"]:
                return "ترجمہ نہیں کیا جا سکا"  # "Translation could not be performed" in Urdu

            return result
        except Exception as e:
            error_msg = str(e).lower()
            # Return appropriate Urdu error message based on the error
            if "quota" in error_msg or "exceeded" in error_msg:
                return "ترجمہ کی سروس کوٹا سے تجاوز کر گیا ہے"  # "Translation service quota exceeded" in Urdu
            elif "api" in error_msg or "key" in error_msg or "auth" in error_msg:
                return "ترجمہ کی سروس کی تشکیل درست نہیں ہے"  # "Translation service is not properly configured" in Urdu
            else:
                return "ترجمہ کے دوران خرابی آ گئی"  # "An error occurred during translation" in Urdu

    @staticmethod
    def run_personalizer(markdown: str, profile: Dict) -> str:
        """Personalize content based on user profile using the personalization agent"""
        try:
            python_knowledge = profile.get('python_knowledge', False)
            has_nvidia_gpu = profile.get('has_nvidia_gpu', False)
            experience_level = profile.get('experience_level', 'beginner')
            system = "You are an educational content personalizer. Adapt the content to match the user's profile, considering their Python knowledge, hardware, and experience level. Make it more accessible for beginners and add depth for advanced users."
            user = f"""Personalize the following textbook content based on the user profile:

User Profile:
- Python Knowledge: {'Yes' if python_knowledge else 'No'}
- Has NVIDIA GPU: {'Yes' if has_nvidia_gpu else 'No'}
- Experience Level: {experience_level}

Content to personalize:
{markdown}

Return a personalized version appropriate for this user's profile. Make it more accessible for beginners, add depth for advanced users, and include relevant examples."""
            return llm_complete(system, user, temperature=0.7, max_tokens=1500)
        except Exception as e:
            raise RuntimeError(f"Personalization failed: {str(e)}")