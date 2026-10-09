from app.database import SessionLocal
from app.models import Student


db = SessionLocal()


student = db.query(Student).filter(
    Student.email == "student@demo.com"
).first()


if not student:

    student = Student(
        name="Demo Student",
        email="student@demo.com",
        password="demo123",
        grade="10"
    )

    db.add(student)
    db.commit()
    db.refresh(student)


print("Student ID:", student.id)
print("Name:", student.name)
print("Email:", student.email)


db.close()