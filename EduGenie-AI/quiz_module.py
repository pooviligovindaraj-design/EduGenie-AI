from ai_service import generate_json


def generate_quiz(text: str, level: str) -> dict:
    return generate_json(
        f"Create exactly 3 multiple-choice questions for a {level} learner from the "
        "material below. Return only valid JSON with this shape: "
        '{"questions":[{"question":"...","options":["...","...","...","..."],'
        '"correct_answer":"...","explanation":"..."}]}. '
        f"The correct_answer must exactly match one option.\n\nMaterial:\n{text}"
    )