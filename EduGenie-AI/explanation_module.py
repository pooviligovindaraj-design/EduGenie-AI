from ai_service import generate_text


def explain_concept(topic: str, level: str, style: str) -> str:
    return generate_text(
        f"Explain the following concept to a {level} learner in a {style} style. "
        f"Use a useful example and avoid unexplained jargon.\n\nConcept: {topic}"
    )