from typing import Literal

from pydantic import BaseModel, Field


Level = Literal["beginner", "intermediate", "advanced"]


class QARequest(BaseModel):
    question: str = Field(min_length=1)
    level: Level = "beginner"


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=1)
    level: Level = "beginner"
    style: str = "simple"


class QuizRequest(BaseModel):
    text: str = Field(min_length=1)
    level: Level = "beginner"


class SummaryRequest(BaseModel):
    text: str = Field(min_length=1)
    length: Literal["short", "medium", "long"] = "medium"
    level: Level = "beginner"


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1)
    level: Level = "beginner"
    hours_per_week: int = Field(default=5, ge=1, le=60)


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=2)
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool