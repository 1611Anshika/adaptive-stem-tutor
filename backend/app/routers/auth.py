
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from pwdlib import PasswordHash

from ..database import get_db
from ..models import Student
from ..security import create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

password_hash = PasswordHash.recommended()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    grade: int

class TeacherRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def verify_password(plain_password: str, stored_password: str) -> bool:
    # Verify modern Argon2 password hashes.
    if stored_password.startswith(("$argon2id$", "$argon2i$", "$argon2d$")):
        try:
            return password_hash.verify(plain_password, stored_password)
        except Exception:
            return False

    # Temporary compatibility for existing plaintext accounts.
    return plain_password == stored_password


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    email = str(data.email).strip().lower()

    existing_student = db.query(Student).filter(
        Student.email == email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    student = Student(
        name=data.name.strip(),
        email=email,
        password=password_hash.hash(data.password),
        grade=str(data.grade),
        role="student"
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "message": "Registration successful",
        "access_token": create_access_token(student),
        "token_type": "bearer",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "role": student.role
        }
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    email = str(data.email).strip().lower()

    student = db.query(Student).filter(
        Student.email == email
    ).first()

    if not student or not verify_password(
        data.password, student.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Upgrade legacy plaintext passwords after successful login.
    if not student.password.startswith(
        ("$argon2id$", "$argon2i$", "$argon2d$")
    ):
        student.password = password_hash.hash(data.password)
        db.commit()
        db.refresh(student)

    return {
        "message": "Login successful",
        "access_token": create_access_token(student),
        "token_type": "bearer",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "role": student.role
        }
    }
@router.post("/teacher/register")
def register_teacher(
    data: TeacherRegisterRequest,
    db: Session = Depends(get_db)
):
    email = str(data.email).strip().lower()

    existing_user = db.query(Student).filter(
        Student.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    teacher = Student(
        name=data.name.strip(),
        email=email,
        password=password_hash.hash(data.password),
        grade=None,
        role="teacher"
    )

    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    return {
        "message": "Teacher registration successful",
        "access_token": create_access_token(teacher),
        "token_type": "bearer",
        "student": {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "grade": teacher.grade,
            "role": teacher.role
        }
    }