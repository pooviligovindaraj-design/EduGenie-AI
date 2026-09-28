from ai_service import generate_text


def answer_question(question: str, level: str) -> str:
    return generate_text(
        f"Answer this educational question for a {level} learner. "
        f"Be accurate, clear, and concise.\n\nQuestion: {question}"
    )