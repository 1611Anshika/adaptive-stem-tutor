from app.database import SessionLocal
from app.models import QuizAttempt

db = SessionLocal()

deleted = db.query(QuizAttempt).delete()

db.commit()
db.close()

print(f"Deleted {deleted} old quiz attempts.")