from pydantic import BaseModel
from typing import List


class AssessmentAnswer(BaseModel):
    question_id: int
    selected_answer: str


class AssessmentSubmission(BaseModel):
    student_id: int
    answers: List[AssessmentAnswer]

class QuizAnswer(BaseModel):
    student_id: int
    question_id: int
    selected_answer: str
    response_time: float | None = None