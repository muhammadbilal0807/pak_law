from google import genai
from config.settings import PRIMARY_MODEL

def get_ai_response(prompt: str) -> str:
    """Sends a user prompt to the Gemini API and returns the text response."""
    client = genai.Client()
    response = client.models.generate_content(
        model=PRIMARY_MODEL,
        contents=prompt,
    )
    return response.text