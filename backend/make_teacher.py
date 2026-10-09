
from getpass import getpass

from app.database import SessionLocal
from app.models import Student


def main():
    email = input("Enter the existing teacher account email: ").strip().lower()
    db = SessionLocal()

    try:
        account = db.query(Student).filter(
            Student.email == email
        ).first()

        if not account:
            print("Account not found. Register it first.")
            return

        account.role = "teacher"
        db.commit()
        print(f"Teacher role assigned to {account.email}.")

    finally:
        db.close()


if __name__ == "__main__":
    main()