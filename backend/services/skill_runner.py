import json
import os
from typing import Dict
import google.generativeai as genai
from config import API_KEY

class SkillRunner:
    """Service for invoking agent skills directly (avoiding subprocess encoding issues)"""

    @staticmethod
    def _get_model():
        """Get configured Gemini model"""
        if not API_KEY:
            raise RuntimeError("API_KEY not configured")
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-2.5-flash')

    @staticmethod
    def run_quiz_generator(markdown: str) -> str:
        """Generate quiz for chapter markdown using the quiz agent"""
        try:
            model = SkillRunner._get_model()

            prompt = f"""
            Generate a quiz based on the following textbook content.
            Create 5 multiple-choice questions with 4 options each.
            Include the correct answer for each question.
            Format the output as clear questions with options and answers.

            Textbook content:
            {markdown}

            Please provide the quiz in a clear, formatted way.
            """

            response = model.generate_content(prompt)

            # Handle response properly
            if response.text:
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content.parts:
                    text_content = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    return text_content or "Quiz could not be generated."

            return "Quiz could not be generated."

        except Exception as e:
            raise RuntimeError(f"Quiz generation failed: {str(e)}")

    @staticmethod
    def run_translator(markdown: str) -> str:
        """Translate markdown to Urdu using the translation agent"""
        try:
            model = SkillRunner._get_model()

            prompt = f"""
            Translate the following English text to Urdu.
            Preserve the meaning and context accurately.
            Make sure technical terms are appropriately translated or kept in English if there's no direct Urdu equivalent.

            Text to translate:
            {markdown}

            Please provide only the translated text in Urdu, nothing else.
            """

            response = model.generate_content(prompt)

            # Handle response properly
            if response.text:
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content.parts:
                    text_content = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    return text_content or "Translation could not be generated."

            return "Translation could not be generated."

        except Exception as e:
            raise RuntimeError(f"Translation failed: {str(e)}")

    @staticmethod
    def run_personalizer(markdown: str, profile: Dict) -> str:
        """Personalize content based on user profile using the personalization agent"""
        try:
            model = SkillRunner._get_model()

            python_knowledge = profile.get('python_knowledge', False)
            has_nvidia_gpu = profile.get('has_nvidia_gpu', False)
            experience_level = profile.get('experience_level', 'beginner')

            prompt = f"""
            Personalize the following textbook content based on the user profile:

            User Profile:
            - Python Knowledge: {'Yes' if python_knowledge else 'No'}
            - Has NVIDIA GPU: {'Yes' if has_nvidia_gpu else 'No'}
            - Experience Level: {experience_level}

            Content to personalize:
            {markdown}

            Please return a personalized version of the content that is appropriate for this user's profile.
            Make it more accessible if they're beginners, add more depth if they're advanced,
            and include relevant examples based on their background.
            """

            response = model.generate_content(prompt)

            # Handle response properly
            if response.text:
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content.parts:
                    text_content = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    return text_content or "Personalization could not be generated."

            return "Personalization could not be generated."

        except Exception as e:
            raise RuntimeError(f"Personalization failed: {str(e)}")