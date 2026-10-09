from sqlalchemy.orm import Session

from ..models import StudentMastery


def generate_tutor_response(
    student_id: int,
    question,
    is_correct: bool,
    db: Session
):

    mastery = db.query(StudentMastery).filter(
        StudentMastery.student_id == student_id,
        StudentMastery.topic_id == question.topic_id
    ).first()

    mastery_score = (
        mastery.mastery_score * 100
        if mastery
        else 0
    )

    topic = question.topic.name
    difficulty = question.difficulty.lower()

    if is_correct:

        if mastery_score >= 70:

            response = (
                f"Excellent work! You are showing strong "
                f"understanding of {topic}. Since you handled "
                f"a {difficulty} question correctly, you are "
                f"ready for a greater challenge."
            )

        else:

            response = (
                f"Good job! You correctly solved this "
                f"{difficulty} {topic} question. "
                f"Keep practicing to strengthen your mastery."
            )

    else:

        response = (
            f"Let's work through this {topic} question "
            f"step by step. Don't worry about the mistake — "
            f"an incorrect answer helps identify what needs "
            f"more practice."
        )

    return {
        "message": response,
        "topic": topic,
        "difficulty": difficulty,
        "mastery_score": round(mastery_score, 1),
        "explanation": question.explanation
    }