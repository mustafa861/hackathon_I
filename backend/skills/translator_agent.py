#!/usr/bin/env python3
"""
Translator agent for the Smart Textbook Platform
This agent translates content to Urdu
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
        # Create a prompt for translation
        prompt = f"""
        Translate the following English text to Urdu.
        Preserve the meaning and context accurately.
        Make sure technical terms are appropriately translated or kept in English if there's no direct Urdu equivalent.

        Text to translate:
        {input_text}

        Please provide only the translated text in Urdu, nothing else.
        """

        # Use the Gemini model to translate content
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
                    output_text = text_content or "Translation could not be generated."
                else:
                    output_text = "Translation could not be generated."
            else:
                output_text = "Translation could not be generated."

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
                print("Translation result contains special characters that cannot be displayed.")

    except Exception as e:
        print(f"Error in translation: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()