from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from sqlalchemy import UniqueConstraint
from sqlalchemy import Date

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    grade = Column(String, nullable=True)

    attempts = relationship("QuizAttempt", back_populates="student")
    mastery = relationship("StudentMastery", back_populates="student")
    role = Column(String, default="student", nullable=False)


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

    questions = relationship("Question", back_populates="topic")
    mastery = relationship("StudentMastery", back_populates="topic")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    question_text = Column(Text, nullable=False)

    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)

    correct_answer = Column(String, nullable=False)

    difficulty = Column(String, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))

    explanation = Column(Text, nullable=True)

    topic = relationship("Topic", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    selected_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    response_time = Column(Float, nullable=True)

    student = relationship("Student", back_populates="attempts")


class StudentMastery(Base):
    __tablename__ = "student_mastery"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    mastery_score = Column(Float, default=0.0)

    student = relationship("Student", back_populates="mastery")
    topic = relationship("Topic", back_populates="mastery")


class RevisionTask(Base):
    __tablename__ = "revision_tasks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )
    topic_id = Column(
        Integer,
        ForeignKey("topics.id"),
        nullable=False
    )
    is_completed = Column(Boolean, default=False, nullable=False)

    
class RevisionActivity(Base):
    __tablename__ = "revision_activities"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    activity_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "activity_date",
            name="unique_student_revision_date"
        ),
    )
    
class StudentGamification(Base):
    __tablename__ = "student_gamification"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        unique=True,
        index=True
    )

    total_xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)

    student = relationship("Student")


class StudentAchievement(Base):
    __tablename__ = "student_achievements"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        index=True
    )

    achievement_code = Column(String, nullable=False)
    earned_at = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "achievement_code",
            name="unique_student_achievement"
        ),
    )

    student = relationship("Student")