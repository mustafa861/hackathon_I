#!/usr/bin/env python3
"""
Agent Skill: Content Personalizer
Rewrites content based on user profile (Python/C++ knowledge, GPU availability).
Constitution Principle II: Reusable Intelligence (CLI tool pattern)
"""

import sys
import json
import google.generativeai as genai
import os

def personalize_content(markdown: str, profile: dict) -> str:
    """Rewrite content tailored to user's technical background"""

    if not markdown.strip():
        raise ValueError("Empty content")
    if not profile:
        raise ValueError("Empty profile")

    # Build profile description
    bg_desc = []
    if profile.get("python_knowledge"):
        bg_desc.append("proficient in Python")
    if profile.get("has_nvidia_gpu"):
        bg_desc.append("has access to NVIDIA GPU hardware")

    experience = profile.get("experience_level", "intermediate")
    bg_str = ", ".join(bg_desc) if bg_desc else "no specific programming background"

    prompt = f"""You are rewriting educational robotics content for a student who is {bg_str} with {experience} experience level.

INSTRUCTIONS:
1. Adapt explanations and analogies to match the student's background
2. If student knows Python: use Python-specific analogies (e.g., "like a generator", "similar to asyncio")
3. If student has GPU: mention GPU-accelerated computing opportunities where relevant
4. If beginner: add more foundational context; if advanced: assume prerequisite knowledge
5. Preserve ALL markdown formatting (headings, code blocks, LaTeX equations, lists)
6. Keep the same structure and length (don't add new major sections)
7. Use at least 3 personalized analogies or references based on their profile

Original content:
{markdown}

Rewrite this content tailored to the student's profile.
"""

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")  # Using same env var name for consistency
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7
        )
    )

    personalized = response.text
    return personalized

def main():
    try:
        # Read JSON input from stdin
        input_json = sys.stdin.read()
        data = json.loads(input_json)

        content = data.get("content", "")
        profile = data.get("profile", {})

        output = personalize_content(content, profile)
        print(output, end='')
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()