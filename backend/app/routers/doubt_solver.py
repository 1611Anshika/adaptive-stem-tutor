
import requests

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student
from ..security import get_current_user


router = APIRouter(prefix="/api/doubt-solver", tags=["AI Doubt Solver"])


class DoubtRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    topic: str = Field(default="General Mathematics", max_length=100)
    grade: str = Field(default="school level", max_length=50)


@router.post("/ask")
def ask_doubt(
    request: DoubtRequest,
    current_user: Student = Depends(get_current_user),
):
    prompt = f"""
You are a friendly AI STEM tutor helping a student learn.

Student grade: {request.grade}
Topic: {request.topic}
Student question: {request.question}

Instructions:
1. Explain the concept in simple, student-friendly language.
2. Solve numerical problems step by step.
3. Explain why each step is performed.
4. Include a short example when useful.
5. End with one short practice question.
6. If the question is unrelated to STEM learning, politely guide
   the student back to a learning-related question.
7. Do not invent facts. If something is unclear, say so.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()

        answer = result.get("response", "").strip()

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The AI model returned an empty response.",
            )

        return {
            "question": request.question,
            "topic": request.topic,
            "answer": answer,
            "model": "qwen2.5:3b",
        }

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The AI took too long to respond. Please try again.",
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Please make sure it is running.",
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to get a response from the local AI model.",
        )