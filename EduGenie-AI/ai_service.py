import json
import time
from google import genai
from google.genai.errors import APIError
from config import settings


def generate_text(prompt: str, max_retries: int = 3) -> str:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to .env and restart the server."
        )

    client = genai.Client(api_key=settings.gemini_api_key)

    # Automatic retry loop for temporary server overloads (503 / 429)
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )
            text = (response.text or "").strip()
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text

        except APIError as exc:
            # If server is busy (503) or rate-limited (429), retry after a short delay
            if getattr(exc, "code", None) in [503, 429] and attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))  # Waits 2s, then 4s
                continue
            raise exc


def generate_json(prompt: str) -> dict:
    text = generate_text(prompt)

    # Clean markdown code block formatting safely
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid quiz data.") from exc

    if not isinstance(value, dict):
        raise RuntimeError("Gemini returned an invalid quiz response.")

    return value