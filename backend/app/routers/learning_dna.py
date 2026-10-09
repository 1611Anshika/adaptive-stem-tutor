
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Student, StudentMastery, Topic, Question, QuizAttempt
from ..security import get_current_user


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Learning DNA"]
)


@router.get("/{student_id}/learning-dna")
def get_learning_dna(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    # Allow students to view their own profile.
    # Teachers can view student profiles for analysis.
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own Learning DNA profile"
        )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    mastery_records = db.query(StudentMastery).filter(
        StudentMastery.student_id == student_id
    ).all()

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).order_by(QuizAttempt.id.asc()).all()

    # Summarize accuracy by topic.
    topic_stats = defaultdict(
        lambda: {"attempts": 0, "correct": 0}
    )

    repeated_errors = defaultdict(
        lambda: {"count": 0, "question": None, "topic": "Unknown"}
    )

    for attempt in attempts:
        question = db.query(Question).filter(
            Question.id == attempt.question_id
        ).first()

        if not question:
            continue

        topic = db.query(Topic).filter(
            Topic.id == question.topic_id
        ).first()

        topic_name = topic.name if topic else "Unknown"

        topic_stats[topic_name]["attempts"] += 1

        if attempt.is_correct:
            topic_stats[topic_name]["correct"] += 1
        else:
            item = repeated_errors[question.id]
            item["count"] += 1
            item["question"] = question.question_text
            item["topic"] = topic_name

    # Include mastery and accuracy in the same topic profile.
    mastery_by_topic = {}

    for record in mastery_records:
        topic = db.query(Topic).filter(
            Topic.id == record.topic_id
        ).first()

        if topic:
            mastery_by_topic[topic.name] = round(
                record.mastery_score * 100, 1
            )

    topic_profiles = []

    for topic_name, stats in topic_stats.items():
        total = stats["attempts"]
        correct = stats["correct"]

        topic_profiles.append({
            "topic": topic_name,
            "attempts": total,
            "correct_answers": correct,
            "accuracy": round(correct / total * 100, 1),
            "mastery": mastery_by_topic.get(topic_name, None)
        })

    # Use the latest ten attempts to summarize recent accuracy.
    recent_attempts = list(reversed(attempts[-10:]))

    if recent_attempts:
        recent_accuracy = round(
            sum(1 for a in recent_attempts if a.is_correct)
            / len(recent_attempts) * 100,
            1
        )
    else:
        recent_accuracy = None

    # Only flag questions answered incorrectly more than once.
    recurring_mistakes = [
        {
            "question_id": question_id,
            "question": data["question"],
            "topic": data["topic"],
            "incorrect_attempts": data["count"]
        }
        for question_id, data in repeated_errors.items()
        if data["count"] >= 2
    ]

    recurring_mistakes.sort(
        key=lambda item: item["incorrect_attempts"],
        reverse=True
    )

    
    recommendations = []

    # Detect topic-level patterns across different questions.
    topic_errors = defaultdict(
        lambda: {
            "attempts": 0,
            "incorrect": 0,
            "incorrect_question_ids": set()
        }
    )

    for attempt in attempts:
        question = db.query(Question).filter(
            Question.id == attempt.question_id
        ).first()

        if not question:
            continue

        topic = db.query(Topic).filter(
            Topic.id == question.topic_id
        ).first()

        if not topic:
            continue

        stats = topic_errors[topic.name]
        stats["attempts"] += 1

        if not attempt.is_correct:
            stats["incorrect"] += 1
            stats["incorrect_question_ids"].add(question.id)

    mistake_patterns = []

    for topic_name, stats in topic_errors.items():
        total = stats["attempts"]
        incorrect = stats["incorrect"]
        error_rate = incorrect / total if total else 0

        # Require at least three attempts before flagging a pattern.
        if total >= 3 and error_rate >= 0.50:
            mistake_patterns.append({
                "topic": topic_name,
                "attempts": total,
                "incorrect_attempts": incorrect,
                "distinct_questions_missed": len(
                    stats["incorrect_question_ids"]
                ),
                "error_rate": round(error_rate * 100, 1),
                "pattern": "Repeated difficulty in this topic"
            })

            recommendations.append({
                "topic": topic_name,
                "reason": (
                    f"You answered {incorrect} out of {total} "
                    f"attempts incorrectly in {topic_name}. "
                    "Review the underlying concepts and practice "
                    "different questions from this topic."
                )
            })

    # Keep the existing low-accuracy recommendations.
    for profile in topic_profiles:
        if profile["accuracy"] < 50:
            recommendations.append({
                "topic": profile["topic"],
                "reason": (
                    f"Your accuracy is {profile['accuracy']}% "
                    "in this topic. Review the fundamentals and "
                    "practice similar questions."
                )
            })

    # Keep the existing exact-question repeated-error recommendations.
    for mistake in recurring_mistakes:
        recommendations.append({
            "topic": mistake["topic"],
            "reason": (
                "You have answered the same question incorrectly "
                f"{mistake['incorrect_attempts']} times. "
                "Review its explanation and retry a similar question."
            )
        })

    return {
        "student": {
            "id": student.id,
            "name": student.name
        },
        "learning_profile": {
            "total_attempts": len(attempts),
            "recent_accuracy": recent_accuracy,
            "topic_profiles": topic_profiles,
            "recurring_mistakes": recurring_mistakes,
            "mistake_patterns": mistake_patterns,
            "recommendations": recommendations
        }
    }

    return {
        "student": {
            "id": student.id,
            "name": student.name
        },
        "learning_profile": {
            "total_attempts": len(attempts),
            "recent_accuracy": recent_accuracy,
            "topic_profiles": topic_profiles,
            "recurring_mistakes": recurring_mistakes,
            "recommendations": recommendations
        }
    }