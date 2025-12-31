#!/usr/bin/env python3
"""
Quiz generator agent for the Smart Textbook Platform
This agent generates quizzes from textbook content
"""
import sys
import os
import io
import google.generativeai as genai

def main():
    # Get the API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Configure the Google Generative AI
    genai.configure(api_key=api_key)

    # Get input text
    input_text = sys.stdin.read().strip()

    try:
        # Create a prompt for quiz generation
        prompt = f"""
        Generate a quiz based on the following textbook content.
        Create 5 multiple-choice questions with 4 options each.
        Include the correct answer for each question.
        Format the output as clear questions with options and answers.

        Textbook content:
        {input_text}

        Please provide the quiz in a clear, formatted way.
        """

        # Use the Gemini model to generate quiz
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        # Handle the case where response.text might be empty
        output_text = ""
        if response.text:
            output_text = response.text
        else:
            # If the text is empty, try to get the parts
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content.parts:
                    text_content = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    output_text = text_content or "Quiz could not be generated."
                else:
                    output_text = "Quiz could not be generated."
            else:
                output_text = "Quiz could not be generated."

        # Safe output approach that handles encoding issues
        # Write directly to stdout buffer to avoid encoding issues
        try:
            # Try to print normally first
            print(output_text)
        except (UnicodeEncodeError, UnicodeDecodeError, OSError, AttributeError):
            # If that fails due to encoding, write as bytes directly
            try:
                if hasattr(sys.stdout, 'buffer'):
                    sys.stdout.buffer.write(output_text.encode('utf-8', errors='replace'))
                    sys.stdout.buffer.write(b'\n')  # Add newline
                    sys.stdout.flush()
                else:
                    # Fallback: print with error handling
                    print(output_text.encode('utf-8', errors='replace').decode('utf-8'))
            except:
                # Last resort: print a safe ASCII message
                print("Quiz result contains special characters that cannot be displayed.")

    except Exception as e:
        print(f"Error in quiz generation: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()