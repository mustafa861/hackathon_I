#!/usr/bin/env python3
"""
Quiz generator agent for the Smart Textbook Platform
This agent generates quizzes from textbook content using Google's Gemini
"""
import sys
import os
import google.generativeai as genai

def generate_quiz(content, api_key):
    """
    Generate quiz from textbook content using Google's Gemini
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Generate a quiz based on the following textbook content.
    Create 5 multiple-choice questions with 4 options each.
    Include the correct answer for each question.
    Format the output as clear questions with options and answers.

    Textbook content:
    {content}

    Please provide the quiz in a clear, formatted way.
    """

    response = model.generate_content(prompt)

    if response.text:
        return response.text
    else:
        return "Quiz could not be generated."

def main():
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Get input text from stdin
    input_text = sys.stdin.read().strip()

    try:
        result = generate_quiz(input_text, api_key)
        print(result)
    except Exception as e:
        print(f"Quiz generation error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()