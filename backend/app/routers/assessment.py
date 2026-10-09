from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student, Question, StudentMastery, Topic
from ..schemas import AssessmentSubmission
from ..security import get_current_user


router = APIRouter(
    prefix="/api/assessment",
    tags=["Diagnostic Assessment"]
)

@router.get("/questions")
def get_assessment_questions(
    subject: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    query = db.query(Question).join(Topic)

    if subject:
        query = query.filter(Topic.subject.ilike(subject.strip()))

    questions = query.all()

    return [
        {
            "id": q.id,
            "question_text": q.question_text,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "difficulty": q.difficulty,
            "topic": q.topic.name,
            "subject": q.topic.subject
        }
        for q in questions
    ]


@router.post("/submit")
def submit_assessment(
    submission: AssessmentSubmission,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    if current_user.role != "teacher" and current_user.id != submission.student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only submit an assessment for your own account"
        )

    student = db.query(Student).filter(
        Student.id == submission.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    topic_results = {}

    for answer in submission.answers:

        question = db.query(Question).filter(
            Question.id == answer.question_id
        ).first()

        if not question:
            continue

        is_correct = (
            answer.selected_answer.upper()
            == question.correct_answer.upper()
        )

        
        # Topic statistics
        topic_name = question.topic.name

        if topic_name not in topic_results:
            topic_results[topic_name] = {
                "correct": 0,
                "total": 0
            }

        topic_results[topic_name]["total"] += 1

        if is_correct:
            topic_results[topic_name]["correct"] += 1

    # Calculate mastery
    mastery_results = []

    for topic_name, result in topic_results.items():

        score = (
            result["correct"] / result["total"]
        )

        topic = db.query(Topic).filter(
            Topic.name == topic_name
        ).first()

        existing_mastery = db.query(StudentMastery).filter(
            StudentMastery.student_id == student.id,
            StudentMastery.topic_id == topic.id
        ).first()

        if existing_mastery:

            existing_mastery.mastery_score = score

        else:

            mastery = StudentMastery(
                student_id=student.id,
                topic_id=topic.id,
                mastery_score=score
            )

            db.add(mastery)

        if score < 0.50:
            level = "Weak"
        elif score < 0.75:
            level = "Needs Practice"
        else:
            level = "Strong"

        mastery_results.append({
            "topic": topic_name,
            "score": round(score * 100, 2),
            "level": level
        })

    db.commit()

    overall_score = 0

    if mastery_results:
        overall_score = sum(
            result["score"]
            for result in mastery_results
        ) / len(mastery_results)

    weak_topics = [
        result["topic"]
        for result in mastery_results
        if result["level"] == "Weak"
    ]

    return {
        "message": "Assessment completed successfully",

        "student_id": student.id,

        "overall_score": round(overall_score, 2),

        "topic_results": mastery_results,

        "weak_topics": weak_topics
    }