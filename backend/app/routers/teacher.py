
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    Student,
    StudentMastery,
    QuizAttempt,
    Topic
)
from ..security import require_teacher

router = APIRouter(
    prefix="/api/teacher",
    tags=["Teacher Dashboard"],
    dependencies=[Depends(require_teacher)],
)


@router.get("/overview")
def get_teacher_overview(
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()
    attempts = db.query(QuizAttempt).all()
    mastery_records = db.query(StudentMastery).all()

    total_attempts = len(attempts)

    correct_answers = sum(
        1 for attempt in attempts
        if attempt.is_correct
    )

    accuracy = (
        correct_answers / total_attempts * 100
        if total_attempts else 0
    )

    average_mastery = (
        sum(m.mastery_score for m in mastery_records)
        / len(mastery_records) * 100
        if mastery_records else 0
    )

    return {
        "total_students": len(students),
        "total_questions_attempted": total_attempts,
        "class_accuracy": round(accuracy, 1),
        "average_mastery": round(average_mastery, 1)
    }


@router.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()
    result = []

    for student in students:
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == student.id
        ).all()

        mastery_records = db.query(
            StudentMastery
        ).filter(
            StudentMastery.student_id == student.id
        ).all()

        total = len(attempts)
        correct = sum(
            1 for attempt in attempts
            if attempt.is_correct
        )

        accuracy = (
            correct / total * 100
            if total else 0
        )

        average_mastery = (
            sum(m.mastery_score for m in mastery_records)
            / len(mastery_records) * 100
            if mastery_records else 0
        )

        weakest_topic = None

        if mastery_records:
            weakest = min(
                mastery_records,
                key=lambda item: item.mastery_score
            )

            topic = db.query(Topic).filter(
                Topic.id == weakest.topic_id
            ).first()

            if topic:
                weakest_topic = topic.name

        result.append({
            "id": student.id,
            "name": student.name,
            "grade": student.grade,
            "questions_attempted": total,
            "accuracy": round(accuracy, 1),
            "average_mastery": round(
                average_mastery, 1
            ),
            "weakest_topic": weakest_topic
        })

    return result


@router.get("/topics")
def get_topic_analytics(
    db: Session = Depends(get_db)
):
    topics = db.query(Topic).all()
    result = []

    for topic in topics:
        mastery_records = db.query(
            StudentMastery
        ).filter(
            StudentMastery.topic_id == topic.id
        ).all()

        average = (
            sum(m.mastery_score for m in mastery_records)
            / len(mastery_records) * 100
            if mastery_records else 0
        )

        result.append({
            "topic": topic.name,
            "subject": topic.subject,
            "students_assessed": len(mastery_records),
            "average_mastery": round(average, 1)
        })

    return result