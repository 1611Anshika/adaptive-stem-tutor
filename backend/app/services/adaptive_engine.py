from sqlalchemy.orm import Session

from ..models import (
    StudentMastery,
    Question,
    Topic,
    QuizAttempt
)


def get_student_mastery(
    student_id: int,
    topic_id: int,
    db: Session
):
    mastery = db.query(StudentMastery).filter(
        StudentMastery.student_id == student_id,
        StudentMastery.topic_id == topic_id
    ).first()

    if mastery:
        return mastery.mastery_score

    return 0.0



def determine_difficulty(
    mastery_score: float,
    recent_accuracy: float | None = None
):
    # Recent performance gets priority
    score = recent_accuracy if recent_accuracy is not None else mastery_score

    if score < 0.40:
        return "easy"
    elif score < 0.60:
        return "medium"
    elif score < 0.80:
        return "hard"
    else:
        return "extreme hard"

    # Fallback to mastery
    if mastery_score < 0.40:
        return "easy"

    elif mastery_score < 0.70:
        return "medium"

    else:
        return "hard"



def get_weakest_topic(
    student_id: int,
    db: Session,
    subject: str | None = None
):
    mastery_query = db.query(StudentMastery).join(
        Topic,
        StudentMastery.topic_id == Topic.id
    ).filter(
        StudentMastery.student_id == student_id
    )

    if subject:
        mastery_query = mastery_query.filter(
            Topic.subject.ilike(subject)
        )

    mastery_records = mastery_query.order_by(
        StudentMastery.mastery_score.asc()
    ).all()

    if mastery_records:
        return mastery_records[0].topic

    return None


def get_recent_accuracy(
    student_id: int,
    topic_id: int,
    db: Session,
    limit: int = 5
):

    recent_attempts = (
        db.query(QuizAttempt)
        .join(Question)
        .filter(
            QuizAttempt.student_id == student_id,
            Question.topic_id == topic_id
        )
        .order_by(
            QuizAttempt.id.desc()
        )
        .limit(limit)
        .all()
    )

    if not recent_attempts:
        return None

    correct = sum(
        1
        for attempt in recent_attempts
        if attempt.is_correct
    )

    return correct / len(recent_attempts)



def get_adaptive_question(
    student_id: int,
    db: Session,
    subject: str | None = None
):
    # Find all questions this student has already attempted.
    
    # Find questions attempted by this student.
    attempted_query = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    )

    if subject:
        attempted_query = attempted_query.join(
            Question,
            QuizAttempt.question_id == Question.id
        ).join(
            Topic,
            Question.topic_id == Topic.id
        ).filter(
            Topic.subject.ilike(subject)
        )

    attempted_ids = {
        attempt.question_id
        for attempt in attempted_query.all()
    }
    # Helper query: only return questions not yet attempted.
    available_questions = db.query(Question)

    # Filter questions by subject when one is selected.
    if subject:
        available_questions = available_questions.join(
            Topic,
            Question.topic_id == Topic.id
        ).filter(
            Topic.subject.ilike(subject)
        )

    if attempted_ids:
        available_questions = available_questions.filter(
            ~Question.id.in_(attempted_ids)
        )

    # If there are no unattempted questions left, finish the session.
    if not available_questions.first():
        if subject:
            return None, (
                f"You have completed all available questions "
                f"for {subject}."
            )

        return None, "You have completed all available questions."

    weakest_topic = get_weakest_topic(
        student_id,
        db,
        subject=subject
    )

    # No mastery records yet: start with an unattempted easy question.
    if not weakest_topic:
        question = available_questions.filter(
            Question.difficulty.ilike("easy")
        ).order_by(Question.id.asc()).first()

        if question:
            return question, "Starting with an easy question."

        # If no easy questions remain, use any unattempted question.
        question = available_questions.order_by(
            Question.id.asc()
        ).first()

        if question:
            return question, (
                f"Starting with an available {question.difficulty} question."
            )

        return None, "No questions available."

    mastery = get_student_mastery(
        student_id,
        weakest_topic.id,
        db
    )

    recent_accuracy = get_recent_accuracy(
        student_id,
        weakest_topic.id,
        db
    )

    difficulty = determine_difficulty(
        mastery,
        recent_accuracy
    )

    # Prioritize unattempted questions in the weakest topic
    # at the recommended difficulty.
    question = available_questions.filter(
        Question.topic_id == weakest_topic.id,
        Question.difficulty.ilike(difficulty)
    ).order_by(Question.id.asc()).first()

    if question:
        reason = (
            f"{weakest_topic.name} needs practice. "
            f"Recommended difficulty: {difficulty}."
        )

        if recent_accuracy is not None:
            reason += (
                f" Recent accuracy: {round(recent_accuracy * 100)}%."
            )

        return question, reason

    # If that difficulty is unavailable, try another unattempted
    # question in the same topic.
    question = available_questions.filter(
        Question.topic_id == weakest_topic.id
    ).order_by(Question.id.asc()).first()

    if question:
        return question, (
            f"{weakest_topic.name} needs practice. "
            f"Using an available {question.difficulty} question."
        )

    # The weakest topic has no suitable unattempted questions.
    # Continue with another available question.
    question = available_questions.order_by(
        Question.id.asc()
    ).first()

    if question:
        return question, (
            f"Continuing with {question.topic.name} "
            f"because it has an unattempted question."
        )

    return None, "You have completed all available questions."