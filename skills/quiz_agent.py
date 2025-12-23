#!/usr/bin/env python3
"""
Agent Skill: Quiz Generator
Reads chapter markdown from stdin, generates 5-question quiz, appends to content.
Constitution Principle II: Reusable Intelligence (CLI tool pattern)
"""

import sys
import json
import google.generativeai as genai
import os

def generate_quiz(markdown_content: str) -> str:
    """Generate 5-question quiz for given markdown content"""

    if not markdown_content.strip():
        raise ValueError("Empty input provided")

    prompt = f"""You are an expert educator creating quiz questions.

Given the following educational content:

{markdown_content}

Generate exactly 5 multiple-choice questions that test understanding of key concepts.

Format each question as:
:::note Question N
What is [question text]?
A) [option]
B) [option]
C) [option]
D) [option]
**Answer**: [correct letter]
:::

Return ONLY the quiz section with heading "## Check Your Understanding" followed by the 5 questions.
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

    quiz_content = response.text
    return markdown_content + "\n\n" + quiz_content

def main():
    try:
        # Read markdown from stdin
        markdown_input = sys.stdin.read()

        # Generate quiz
        output = generate_quiz(markdown_input)

        # Write to stdout
        print(output, end='')
        sys.exit(0)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()