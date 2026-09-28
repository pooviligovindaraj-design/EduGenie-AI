from ai_service import generate_text


def get_learning_recommendations(topic: str, level: str, hours_per_week: int) -> str:
    return generate_text(
        f"Create a practical learning path for {topic}. The learner is at {level} level "
        f"and has {hours_per_week} hours per week. Include an ordered progression, "
        "weekly practice, and useful project ideas."
    )