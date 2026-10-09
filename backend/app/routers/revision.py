
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from datetime import date, timedelta

from ..models import (
    Student,
    StudentMastery,
    Topic,
    RevisionTask,
    RevisionActivity,
)
from ..security import get_current_user

router = APIRouter(
    prefix="/api/revision",
    tags=["Revision Tracker"]
)


def check_student_access(student_id: int, current_user: Student):
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own revision tasks"
        )


def calculate_revision_streaks(
    student_id: int,
    db: Session
):
    activities = (
        db.query(RevisionActivity.activity_date)
        .filter(RevisionActivity.student_id == student_id)
        .order_by(RevisionActivity.activity_date.desc())
        .all()
    )

    dates = sorted(
        {activity[0] for activity in activities},
        reverse=True
    )

    if not dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_active_days": 0
        }

    # Calculate the longest streak.
    longest_streak = 1
    streak = 1

    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            streak += 1
        else:
            streak = 1

        longest_streak = max(longest_streak, streak)

    # Calculate the current streak.
    today = date.today()
    current_streak = 0

    if dates[0] == today or dates[0] == today - timedelta(days=1):
        current_streak = 1

        for i in range(1, len(dates)):
            if dates[i - 1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_active_days": len(dates)
    }

@router.get("/{student_id}")
def get_revision_tasks(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    check_student_access(student_id, current_user)

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    mastery_records = (
        db.query(StudentMastery)
        .filter(StudentMastery.student_id == student_id)
        .order_by(StudentMastery.mastery_score.asc())
        .all()
    )

    tasks = []

    for mastery in mastery_records:
        topic = db.query(Topic).filter(
            Topic.id == mastery.topic_id
        ).first()

        if not topic:
            continue

        task = db.query(RevisionTask).filter(
            RevisionTask.student_id == student_id,
            RevisionTask.topic_id == topic.id
        ).first()

        if not task:
            task = RevisionTask(
                student_id=student_id,
                topic_id=topic.id,
                is_completed=False
            )
            db.add(task)
            db.flush()

        score = mastery.mastery_score

        if score < 0.40:
            priority = "High"
            action = "Review fundamentals and solve 5 basic questions."
            minutes = 30
        elif score < 0.70:
            priority = "Medium"
            action = "Revise key concepts and solve 5 practice questions."
            minutes = 20
        else:
            priority = "Low"
            action = "Review challenging concepts and solve 3 advanced questions."
            minutes = 15

        tasks.append({
            "id": task.id,
            "topic_id": topic.id,
            "topic": topic.name,
            "subject": topic.subject,
            "mastery_score": round(score * 100, 1),
            "priority": priority,
            "recommended_action": action,
            "recommended_time_minutes": minutes,
            "is_completed": task.is_completed
        })

    db.commit()

    completed = sum(1 for task in tasks if task["is_completed"])
    total = len(tasks)

    
    streaks = calculate_revision_streaks(student_id, db)

    return {
        "student_id": student_id,
        "tasks": tasks,
        "total_tasks": total,
        "completed_tasks": completed,
        "progress_percentage": round(
            completed / total * 100, 1
        ) if total else 0,
        "streaks": streaks
    }


@router.patch("/{student_id}/{task_id}")
def update_revision_task(
    student_id: int,
    task_id: int,
    is_completed: bool,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    check_student_access(student_id, current_user)

    task = db.query(RevisionTask).filter(
        RevisionTask.id == task_id,
        RevisionTask.student_id == student_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Revision task not found")

    
    task.is_completed = is_completed

    if is_completed:
        today = date.today()

        activity = db.query(RevisionActivity).filter(
            RevisionActivity.student_id == student_id,
            RevisionActivity.activity_date == today
        ).first()

        if not activity:
            activity = RevisionActivity(
                student_id=student_id,
                activity_date=today
            )
            db.add(activity)

    db.commit()
    db.refresh(task)

    return {
        "message": "Revision progress updated",
        "task_id": task.id,
        "is_completed": task.is_completed
    }