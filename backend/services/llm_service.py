"""LLM service: uses Gemini if GEMINI_API_KEY is set, otherwise Groq (OPENAI_API_KEY)."""
from config import GEMINI_API_KEY, GEMINI_MODEL, API_KEY, LLM_PROVIDER


def complete(system_prompt: str, user_content: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """
    Generate a completion using the configured LLM (Gemini or Groq).
    If Gemini returns 429 (quota exceeded), tries Groq if OPENAI_API_KEY is set.
    Returns the generated text or raises an exception.
    """
    if LLM_PROVIDER == "gemini" and GEMINI_API_KEY:
        try:
            return _complete_gemini(system_prompt, user_content, temperature, max_tokens)
        except Exception as e:
            err_str = str(e)
            # On quota/rate limit, try Groq as fallback if configured
            if ("429" in err_str or "QUOTA" in err_str.upper() or "RATE" in err_str.upper()) and API_KEY:
                try:
                    return _complete_groq(system_prompt, user_content, temperature, max_tokens)
                except Exception as groq_err:
                    # Groq fallback failed (e.g. invalid key); tell caller so user can fix
                    raise RuntimeError(
                        f"Gemini quota exceeded and Groq fallback failed: {groq_err}. "
                        "Check OPENAI_API_KEY in backend/.env is a valid Groq key (console.groq.com)."
                    ) from e
            raise
    if API_KEY:
        return _complete_groq(system_prompt, user_content, temperature, max_tokens)
    raise RuntimeError("No LLM configured. Set GEMINI_API_KEY or OPENAI_API_KEY (Groq) in backend/.env")


def _complete_gemini(system_prompt: str, user_content: str, temperature: float, max_tokens: int) -> str:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = f"{system_prompt}\n\n{user_content}" if system_prompt else user_content
    config = genai.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    response = model.generate_content(prompt, generation_config=config)
    try:
        return response.text or "I couldn't generate a response."
    except (ValueError, AttributeError):
        return "I couldn't generate a response."


def _complete_groq(system_prompt: str, user_content: str, temperature: float, max_tokens: int) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        model="llama-3.3-70b-versatile",  # llama3-70b-8192 was decommissioned Aug 2025
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or "I couldn't generate a response."
