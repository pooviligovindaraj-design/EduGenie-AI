from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from models import (
    ExplainRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    TextResponse,
    QuizResponse,
    HealthResponse,
)

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational assistant built with FastAPI and Gemini.",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name
        },
    )


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return HealthResponse(
        status="ok",
        gemini_configured=bool(settings.gemini_api_key),
    )


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post(
    "/qa",
    response_model=TextResponse
)
async def qa(payload: QARequest):

    try:

        answer = answer_question(
            payload.question,
            payload.level,
        )

        return TextResponse(
            result=answer
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Explain
# ---------------------------------------------------------

@app.post(
    "/explain",
    response_model=TextResponse
)
async def explain(payload: ExplainRequest):

    try:

        explanation = explain_concept(
            payload.topic,
            payload.level,
            payload.style,
        )

        return TextResponse(
            result=explanation
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(payload: QuizRequest):

    try:

        quiz_data = generate_quiz(
            payload.text,
            payload.level,
        )

        return QuizResponse(
            **quiz_data
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

@app.post(
    "/summarize",
    response_model=TextResponse
)
async def summarize(payload: SummaryRequest):

    try:

        summary = summarize_text(
            payload.text,
            payload.length,
            payload.level,
        )

        return TextResponse(
            result=summary
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Learning path
# ---------------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=TextResponse
)
async def learn(payload: LearningPathRequest):

    try:

        recommendations = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.hours_per_week,
        )

        return TextResponse(
            result=recommendations
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )