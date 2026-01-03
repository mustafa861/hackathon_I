#!/usr/bin/env python3
"""
Translator agent for the Smart Textbook Platform
This agent translates content to Urdu using Google's Gemini
"""
import sys
import os
import json
import google.generativeai as genai

def translate_to_urdu(text, api_key):
    """
    Translate English text to Urdu using Google's Gemini
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Translate the following English text to Urdu.
    Preserve the meaning and context accurately.
    Make sure technical terms are appropriately translated or kept in English if there's no direct Urdu equivalent.

    Text to translate:
    {text}

    Please provide only the translated text in Urdu, nothing else.
    """

    response = model.generate_content(prompt)

    if response.text:
        return response.text
    else:
        return "Translation could not be generated."

def main():
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Get input text from stdin
    input_text = sys.stdin.read().strip()

    try:
        result = translate_to_urdu(input_text, api_key)
        print(result)
    except Exception as e:
        print(f"Translation error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()