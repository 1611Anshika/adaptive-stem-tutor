
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import Student


SECRET_KEY = os.getenv("ADAPTIVE_TUTOR_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "Set the ADAPTIVE_TUTOR_SECRET_KEY environment variable "
        "before starting the backend."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 60

bearer_scheme = HTTPBearer()


def create_access_token(student: Student) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_MINUTES
    )

    payload = {
        "sub": str(student.id),
        "role": student.role,
        "exp": expires,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Student:
    token = credentials.credentials
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        student_id = payload.get("sub")

        if not student_id:
            raise unauthorized

        student_id = int(student_id)

    except (JWTError, ValueError, TypeError):
        raise unauthorized

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise unauthorized

    return student


def require_teacher(
    current_user: Student = Depends(get_current_user),
) -> Student:
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )

    return current_user