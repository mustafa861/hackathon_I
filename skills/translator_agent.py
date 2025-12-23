#!/usr/bin/env python3
"""
Agent Skill: Urdu Translator
Translates markdown to Urdu while preserving LaTeX, code blocks, admonitions.
Constitution Principle II: Reusable Intelligence (CLI tool pattern)
"""

import sys
import re
import google.generativeai as genai
import os

def extract_preserve_blocks(markdown: str) -> tuple[str, dict]:
    """Extract code blocks and LaTeX that should not be translated"""
    placeholders = {}
    counter = 0

    # Extract code blocks
    def replace_code(match):
        nonlocal counter
        placeholder = f"___CODE_BLOCK_{counter}___"
        placeholders[placeholder] = match.group(0)
        counter += 1
        return placeholder

    text = re.sub(r'```.*?```', replace_code, markdown, flags=re.DOTALL)

    # Extract LaTeX (both inline and block)
    def replace_latex(match):
        nonlocal counter
        placeholder = f"___LATEX_{counter}___"
        placeholders[placeholder] = match.group(0)
        counter += 1
        return placeholder

    text = re.sub(r'\$\$.*?\$\$|\$.*?\$', replace_latex, text)

    return text, placeholders

def restore_preserved_blocks(text: str, placeholders: dict) -> str:
    """Restore code blocks and LaTeX"""
    for placeholder, original in placeholders.items():
        text = text.replace(placeholder, original)
    return text

def translate_to_urdu(markdown: str) -> str:
    """Translate markdown to Urdu, preserving technical elements"""

    if not markdown.strip():
        raise ValueError("Empty input provided")

    # Preserve code and LaTeX
    text_to_translate, placeholders = extract_preserve_blocks(markdown)

    prompt = f"""Translate the following educational content to Urdu.

RULES:
1. Translate only natural language text (headings, paragraphs, list items)
2. Keep ALL placeholders (___CODE_BLOCK_N___, ___LATEX_N___) EXACTLY as they are
3. Preserve Docusaurus admonition syntax (:::note, :::warning, etc.) but translate inner text
4. Maintain markdown formatting (headings #, lists -, etc.)

Content to translate:
{text_to_translate}
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
            temperature=0.3  # Lower temp for consistent translations
        )
    )

    translated = response.text

    # Restore preserved blocks
    final_output = restore_preserved_blocks(translated, placeholders)

    return final_output

def main():
    try:
        markdown_input = sys.stdin.read()
        output = translate_to_urdu(markdown_input)
        print(output, end='')
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()