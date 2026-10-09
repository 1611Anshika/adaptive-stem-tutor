
from sqlalchemy.orm import Session

from ..models import (
    StudentMastery,
    Topic,
    QuizAttempt,
    Question,
    RevisionTask,
)



def generate_study_plan(student_id: int, db: Session):
    mastery_records = (
        db.query(StudentMastery)
        .filter(StudentMastery.student_id == student_id)
        .order_by(StudentMastery.mastery_score.asc())
        .all()
    )

    study_plan = []

    for mastery in mastery_records:
        topic = (
            db.query(Topic)
            .filter(Topic.id == mastery.topic_id)
            .first()
        )

        if not topic:
            continue
        revision_task = (
            db.query(RevisionTask)
            .filter(
                RevisionTask.student_id == student_id,
                RevisionTask.topic_id == topic.id,
            )
            .first()
        )

        score = mastery.mastery_score or 0.0

        # Fetch this student's attempts for the current topic.
        attempts = (
            db.query(QuizAttempt)
            .join(Question, QuizAttempt.question_id == Question.id)
            .filter(
                QuizAttempt.student_id == student_id,
                Question.topic_id == topic.id,
            )
            .order_by(QuizAttempt.id.desc())
            .all()
        )

        total_attempts = len(attempts)
        correct_attempts = sum(
            1 for attempt in attempts if attempt.is_correct
        )

        accuracy = (
            round(correct_attempts / total_attempts * 100, 1)
            if total_attempts
            else None
        )

        # Use the latest five attempts as a measure of recent performance.
        recent_attempts = attempts[:5]
        recent_accuracy = (
            round(
                sum(1 for attempt in recent_attempts if attempt.is_correct)
                / len(recent_attempts)
                * 100,
                1,
            )
            if recent_attempts
            else None
        )

        # Compare the latest five attempts with the five before them.
        previous_attempts = attempts[5:10]
        previous_accuracy = (
            round(
                sum(1 for attempt in previous_attempts if attempt.is_correct)
                / len(previous_attempts)
                * 100,
                1,
            )
            if previous_attempts
            else None
        )

        if recent_accuracy is None or previous_accuracy is None:
            performance_trend = "Not enough recent data"
        elif recent_accuracy > previous_accuracy:
            performance_trend = "Improving"
        elif recent_accuracy < previous_accuracy:
            performance_trend = "Needs attention"
        else:
            performance_trend = "Stable"

        # Prioritize both low mastery and weak recent performance.
        if (
            score < 0.40
            or (accuracy is not None and accuracy < 50)
            or (recent_accuracy is not None and recent_accuracy < 40)
        ):
            priority = "High"
            level = "Weak"
            action = (
                "Review fundamentals, study worked examples, "
                "and solve 5 basic questions."
            )
            recommended_time = 30
            target_mastery = 60
            reason = (
                "This topic needs attention because your mastery "
                "or quiz performance is low."
            )
            learning_stage = "Rebuild fundamentals"

        elif (
            score < 0.70
            or (accuracy is not None and accuracy < 75)
            or (recent_accuracy is not None and recent_accuracy < 70)
        ):
            priority = "Medium"
            level = "Needs Practice"
            action = (
                "Revise key concepts and solve 5 practice questions."
            )
            recommended_time = 20
            target_mastery = 75
            reason = (
                "Practice this topic to strengthen understanding "
                "and improve consistency."
            )
            learning_stage = "Strengthen understanding"

        else:
            priority = "Low"
            level = "Strong"
            action = (
                "Review challenging concepts and solve 3 advanced questions."
            )
            recommended_time = 15
            target_mastery = 85
            reason = (
                "Your current performance is strong. "
                "Challenge yourself with more difficult questions."
            )
            learning_stage = "Apply and extend"

        # Add recent performance context to the recommendation.
        if performance_trend == "Improving":
            reason += " Your recent performance is improving."
        elif performance_trend == "Needs attention":
            reason += " Your recent results have declined."

        study_plan.append({
            # Existing fields: preserve compatibility with the dashboard.
            "topic_id": topic.id,
            "revision_task_id": revision_task.id if revision_task else None,
            "is_completed": revision_task.is_completed if revision_task else False,
            "topic": topic.name,
            "subject": topic.subject,
            "mastery_score": round(score * 100, 1),
            "accuracy": accuracy,
            "total_attempts": total_attempts,
            "status": level,
            "priority": priority,
            "recommended_action": action,
            "recommended_time_minutes": recommended_time,

            # New personalized learning fields.
            "recent_accuracy": recent_accuracy,
            "previous_accuracy": previous_accuracy,
            "performance_trend": performance_trend,
            "target_mastery": target_mastery,
            "recommendation_reason": reason,
            "learning_stage": learning_stage,
        })

    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    study_plan.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["mastery_score"],
        )
    )

    # Give the student a clear suggested order for the learning session.
    for index, item in enumerate(study_plan, start=1):
        item["sequence"] = index

    return study_plan