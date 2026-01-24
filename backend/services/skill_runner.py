import json
import os
from typing import Dict
from openai import OpenAI
import openai
from config import API_KEY

class SkillRunner:
    """Service for invoking agent skills directly (avoiding subprocess encoding issues)"""

    @staticmethod
    def _get_client():
        """Get configured OpenAI client for Groq API"""
        if not API_KEY:
            raise RuntimeError("API_KEY not configured")
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        return client

    @staticmethod
    def run_quiz_generator(markdown: str) -> str:
        """Generate quiz for chapter markdown using the quiz agent"""
        try:
            client = SkillRunner._get_client()

            prompt = f"""
            Generate a quiz based on the following textbook content.
            Create 5 multiple-choice questions with 4 options each.
            Include the correct answer for each question.
            Format the output as clear questions with options and answers.

            Textbook content:
            {markdown}

            Please provide the quiz in a clear, formatted way.
            """

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational assistant that creates quizzes based on textbook content. Generate 5 multiple-choice questions with 4 options each and indicate the correct answer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192",  # Using a Groq-compatible model
                temperature=0.7,
                max_tokens=1500
            )

            return response.choices[0].message.content or "Quiz could not be generated."

        except Exception as e:
            raise RuntimeError(f"Quiz generation failed: {str(e)}")

    @staticmethod
    def run_translator(markdown: str) -> str:
        """Translate markdown to Urdu using the translation agent"""
        try:
            client = SkillRunner._get_client()

            prompt = f"""
            Translate the following English text to Urdu.
            Preserve the meaning and context accurately.
            Make sure technical terms are appropriately translated or kept in English if there's no direct Urdu equivalent.

            Text to translate:
            {markdown}

            Please provide only the translated text in Urdu, nothing else.
            """

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator that translates English text to Urdu. Maintain accuracy and cultural appropriateness."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192",  # Using a Groq-compatible model
                temperature=0.3,
                max_tokens=1500
            )

            return response.choices[0].message.content or "Translation could not be generated."

        except Exception as e:
            raise RuntimeError(f"Translation failed: {str(e)}")

    @staticmethod
    def run_personalizer(markdown: str, profile: Dict) -> str:
        """Personalize content based on user profile using the personalization agent"""
        try:
            client = SkillRunner._get_client()

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

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content personalizer. Adapt the content to match the user's profile, considering their Python knowledge, hardware, and experience level. Make it more accessible for beginners and add depth for advanced users."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192",  # Using a Groq-compatible model
                temperature=0.7,
                max_tokens=1500
            )

            return response.choices[0].message.content or "Personalization could not be generated."

        except Exception as e:
            raise RuntimeError(f"Personalization failed: {str(e)}")