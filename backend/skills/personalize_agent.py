#!/usr/bin/env python3
"""
Personalize agent for the Smart Textbook Platform
This agent personalizes content based on user profile
"""
import json
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

    # Get input data
    input_text = sys.stdin.read().strip()

    try:
        # Parse the input JSON (it should contain content and profile)
        input_data = json.loads(input_text)
        content = input_data.get('content', '')
        profile = input_data.get('profile', {})

        # Create a prompt for personalization
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

        # Use the Gemini model to personalize content
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
                    output_text = text_content or "Personalization could not be generated."
                else:
                    output_text = "Personalization could not be generated."
            else:
                output_text = "Personalization could not be generated."

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
                print("Personalization result contains special characters that cannot be displayed.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error in personalization: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()