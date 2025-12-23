import subprocess
import json
import os
from typing import Dict

class SkillRunner:
    """Service for invoking agent skills via subprocess (Constitution Principle II)"""

    SKILL_TIMEOUT = 15  # seconds

    @staticmethod
    def run_quiz_generator(markdown: str) -> str:
        """Generate quiz for chapter markdown"""
        env = os.environ.copy()
        env['GOOGLE_API_KEY'] = os.getenv('OPENAI_API_KEY')  # Map to Google API key

        result = subprocess.run(
            ["python", "skills/quiz_agent.py"],
            input=markdown,
            capture_output=True,
            text=True,
            timeout=SkillRunner.SKILL_TIMEOUT,
            env=env
        )

        if result.returncode != 0:
            raise RuntimeError(f"Quiz generation failed: {result.stderr}")

        return result.stdout

    @staticmethod
    def run_translator(markdown: str) -> str:
        """Translate markdown to Urdu"""
        env = os.environ.copy()
        env['GOOGLE_API_KEY'] = os.getenv('OPENAI_API_KEY')  # Map to Google API key

        result = subprocess.run(
            ["python", "skills/translator_agent.py"],
            input=markdown,
            capture_output=True,
            text=True,
            timeout=SkillRunner.SKILL_TIMEOUT,
            env=env
        )

        if result.returncode != 0:
            raise RuntimeError(f"Translation failed: {result.stderr}")

        return result.stdout

    @staticmethod
    def run_personalizer(markdown: str, profile: Dict) -> str:
        """Personalize content based on user profile"""
        input_data = json.dumps({"content": markdown, "profile": profile})

        env = os.environ.copy()
        env['GOOGLE_API_KEY'] = os.getenv('OPENAI_API_KEY')  # Map to Google API key

        result = subprocess.run(
            ["python", "skills/personalize_agent.py"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=SkillRunner.SKILL_TIMEOUT,
            env=env
        )

        if result.returncode != 0:
            raise RuntimeError(f"Personalization failed: {result.stderr}")

        return result.stdout