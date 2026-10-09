
import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "adaptive_tutor.db"

with sqlite3.connect(db_path) as connection:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(students)")
    }

    if "role" not in columns:
        connection.execute(
            "ALTER TABLE students "
            "ADD COLUMN role VARCHAR NOT NULL DEFAULT 'student'"
        )
        print("Migration successful: role column added.")
    else:
        print("The role column already exists. No changes needed.")