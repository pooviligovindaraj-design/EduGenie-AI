from ai_service import generate_text


def summarize_text(
    text: str,
    length: str = "Medium",
    level: str = "Beginner",
) -> str:

    prompt = f"""
You are EduGenie, an AI learning assistant.

Create a clear and useful summary of the following text.

Student level: {level}
Summary length: {length}

Text:
{text}

Instructions:
- Use simple language suitable for the student's level.
- Keep the important points.
- Use headings or bullet points when helpful.
- Do not add information that is not present in the text.
"""

    return generate_text(prompt)