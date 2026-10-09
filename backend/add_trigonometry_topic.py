
from app.database import SessionLocal
from app.models import Topic

db = SessionLocal()

try:
    topic = (
        db.query(Topic)
        .filter(
            Topic.name == "Trigonometry",
            Topic.subject == "Mathematics"
        )
        .first()
    )

    if topic:
        print("Trigonometry topic already exists. No changes made.")
    else:
        topic = Topic(
            name="Trigonometry",
            subject="Mathematics"
        )
        db.add(topic)
        db.commit()
        print("Mathematics → Trigonometry topic added successfully.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()

