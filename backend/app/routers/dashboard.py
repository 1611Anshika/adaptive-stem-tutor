from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    Student,
    StudentMastery,
    Topic,
    QuizAttempt
)
from ..services.recommendation import generate_study_plan
from ..security import get_current_user


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Student Dashboard"]
)


@router.get("/{student_id}")
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own dashboard"
        )

    # Check student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Get mastery records
    mastery_records = db.query(StudentMastery).filter(
        StudentMastery.student_id == student_id
    ).all()

    # Calculate overall mastery
    if mastery_records:
        overall_mastery = sum(
            m.mastery_score for m in mastery_records
        ) / len(mastery_records)
    else:
        overall_mastery = 0.0

    # Get quiz attempts
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    total_attempted = len(attempts)

    correct_answers = sum(
        1 for attempt in attempts
        if attempt.is_correct
    )

    if total_attempted > 0:
        accuracy = (
            correct_answers / total_attempted
        )
    else:
        accuracy = 0.0

    # Topic performance
    topic_performance = []

    for mastery in mastery_records:

        topic = db.query(Topic).filter(
            Topic.id == mastery.topic_id
        ).first()

        if not topic:
            continue

        if mastery.mastery_score < 0.40:
            status = "Weak"

        elif mastery.mastery_score < 0.70:
            status = "Needs Practice"

        else:
            status = "Strong"

        topic_performance.append({
            "topic": topic.name,
            "subject": topic.subject,
            "mastery_score": round(
                mastery.mastery_score * 100, 1
            ),
            "status": status
        })

    # Weak topics
    weak_topics = [
        item["topic"]
        for item in topic_performance
        if item["status"] == "Weak"
    ]

    # Strong topics
    strong_topics = [
        item["topic"]
        for item in topic_performance
        if item["status"] == "Strong"
    ]

    # Personalized study plan
    study_plan = generate_study_plan(
        student_id,
        db
    )

    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "grade": student.grade
        },

        "overall_performance": {
            "overall_mastery": round(
                overall_mastery * 100, 1
            ),
            "quiz_accuracy": round(
                accuracy * 100, 1
            ),
            "questions_attempted": total_attempted,
            "correct_answers": correct_answers
        },

        "weak_topics": weak_topics,

        "strong_topics": strong_topics,

        "topic_performance": topic_performance,

        "study_plan": study_plan
    }


@router.get("/{student_id}/study-plan")
def get_study_plan(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own study plan"
        )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    study_plan = generate_study_plan(
        student_id,
        db
    )

    return {
        "student_id": student_id,
        "student_name": student.name,
        "study_plan": study_plan
    }