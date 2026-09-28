import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def get_int_env(
    name: str,
    default: int
) -> int:

    try:

        return int(
            os.getenv(
                name,
                default
            )
        )

    except (
        TypeError,
        ValueError
    ):

        return default


@dataclass(frozen=True)
class Settings:

    app_name: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    explanation_provider: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    ).lower()

    local_model_name: str = os.getenv(
        "LOCAL_MODEL_NAME",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    max_input_chars: int = get_int_env(
        "MAX_INPUT_CHARS",
        20000
    )

    max_output_tokens: int = get_int_env(
        "MAX_OUTPUT_TOKENS",
        1200
    )


settings = Settings()