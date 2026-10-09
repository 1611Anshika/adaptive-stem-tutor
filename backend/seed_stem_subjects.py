
from app.database import SessionLocal
from app.models import Topic

SUBJECT_TOPICS = {
    "Physics": [
        "Motion",
        "Force and Laws of Motion",
        "Work, Energy and Power",
        "Electricity",
        "Waves and Optics",
    ],
    "Chemistry": [
        "Atomic Structure",
        "Periodic Table",
        "Chemical Reactions",
        "Acids and Bases",
        "Chemical Bonding",
    ],
    "Biology": [
        "Cell Biology",
        "Human Biology",
        "Genetics",
        "Plant Biology",
        "Ecology",
    ],
    "Computer Science": [
        "Programming Fundamentals",
        "Data Structures",
        "Algorithms",
        "Database Management",
        "Computer Networks",
    ],
}


def seed_topics():
    db = SessionLocal()

    try:
        added = 0

        for subject, topic_names in SUBJECT_TOPICS.items():
            for topic_name in topic_names:
                existing = db.query(Topic).filter(
                    Topic.subject == subject,
                    Topic.name == topic_name,
                ).first()

                if existing:
                    continue

                db.add(
                    Topic(
                        name=topic_name,
                        subject=subject,
                    )
                )
                added += 1

        db.commit()
        print(f"Successfully added {added} new topics.")

        for subject in SUBJECT_TOPICS:
            count = db.query(Topic).filter(
                Topic.subject == subject
            ).count()
            print(f"{subject}: {count} topics")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_topics()