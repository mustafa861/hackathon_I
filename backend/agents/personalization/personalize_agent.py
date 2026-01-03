#!/usr/bin/env python3
"""
Personalize agent for the Smart Textbook Platform
This agent personalizes content based on user profile using Google's Gemini
"""
import sys
import os
import json
import google.generativeai as genai

def personalize_content(content, profile, api_key):
    """
    Personalize content based on user profile using Google's Gemini
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

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
    {content}

    Please return a personalized version of the content that is appropriate for this user's profile.
    Make it more accessible if they're beginners, add more depth if they're advanced,
    and include relevant examples based on their background.
    """

    response = model.generate_content(prompt)

    if response.text:
        return response.text
    else:
        return "Personalization could not be generated."

def main():
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Get input JSON from stdin
    input_text = sys.stdin.read().strip()

    try:
        # Parse input JSON
        input_data = json.loads(input_text)
        content = input_data.get('content', '')
        profile = input_data.get('profile', {})

        result = personalize_content(content, profile, api_key)
        print(result)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Personalization error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()