from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    Student,
    Question,
    QuizAttempt,
    StudentMastery
)
from ..schemas import QuizAnswer
from ..services.adaptive_engine import get_adaptive_question
from ..services.tutor import generate_tutor_response
from ..security import get_current_user


router = APIRouter(
    prefix="/api/quiz",
    tags=["Adaptive Quiz"]
)


from fastapi import Query

@router.get("/next/{student_id}")
def get_next_question(
    student_id: int,
    subject: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own quiz"
        )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    question, reason = get_adaptive_question(
            student_id,
            db,
            subject=subject
        )

    if not question:
        return {"message": "No more questions available"}

    return {
        "question_id": question.id,
        "question": question.question_text,
        "options": {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c,
            "D": question.option_d
        },
        "difficulty": question.difficulty,
        "topic": question.topic.name,
        "subject": question.topic.subject,
        "adaptive_reason": reason
    }


@router.post("/answer")
def submit_quiz_answer(
    answer: QuizAnswer,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != answer.student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only submit answers for your own account"
        )

    student = db.query(Student).filter(
        Student.id == answer.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    question = db.query(Question).filter(
        Question.id == answer.question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    is_correct = (
        answer.selected_answer.upper()
        == question.correct_answer.upper()
    )

    # Store attempt
    attempt = QuizAttempt(
        student_id=answer.student_id,
        question_id=answer.question_id,
        selected_answer=answer.selected_answer,
        is_correct=is_correct,
        response_time=answer.response_time
    )

    db.add(attempt)

    # Find existing mastery
    mastery = db.query(StudentMastery).filter(
        StudentMastery.student_id == answer.student_id,
        StudentMastery.topic_id == question.topic_id
    ).first()

    # Difficulty-based mastery adjustment
    difficulty_change = {
        "easy": 0.05,
        "medium": 0.08,
        "hard": 0.12
    }

    change = difficulty_change.get(
        question.difficulty.lower(),
        0.08
    )

    if mastery:

        old_score = mastery.mastery_score

        if is_correct:
            new_score = old_score + change
        else:
            new_score = old_score - change

        mastery.mastery_score = max(
            0.0,
            min(1.0, new_score)
        )

    else:

        # Initial mastery based on first response
        if is_correct:
            initial_score = {
                "easy": 0.55,
                "medium": 0.60,
                "hard": 0.70
            }.get(question.difficulty.lower(), 0.60)

        else:
            initial_score = {
                "easy": 0.30,
                "medium": 0.25,
                "hard": 0.20
            }.get(question.difficulty.lower(), 0.25)

        mastery = StudentMastery(
            student_id=answer.student_id,
            topic_id=question.topic_id,
            mastery_score=initial_score
        )

        db.add(mastery)

    db.commit()

    # Feedback
    tutor_response = generate_tutor_response(
        answer.student_id,
        question,
        is_correct,
        db
    )

    feedback = tutor_response["message"]

    return {
    "correct": is_correct,
    "feedback": feedback,
    "correct_answer": question.correct_answer,
    "topic": question.topic.name,
    "difficulty": question.difficulty,
    "mastery_score": round(
        mastery.mastery_score * 100,
        1
    ),
    "tutor": tutor_response
    }