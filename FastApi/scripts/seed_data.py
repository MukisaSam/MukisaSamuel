"""
scripts/seed_data.py
--------------------
A standalone script you run MANUALLY to fill the database with a few
demo students. It is NOT part of the running app.

Order of operations for a fresh setup:
    1. alembic upgrade head        # create the tables (Alembic)
    2. python -m scripts.seed_data # add the demo students (this file)

Run it from the project root as a module:
    python -m scripts.seed_data

(Running `python scripts/seed_data.py` directly also works, thanks to the
sys.path line below that makes the project importable either way.)
"""

import sys
from pathlib import Path

# Make sure the project root is on the import path, so "import app" works
# no matter how this script is launched.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import crud
from app.db.session import SessionLocal
from app.schemas.student import StudentCreate

# The demo data. Add or edit rows here.
SAMPLE_STUDENTS = [
    StudentCreate(name="Mukisa Samuel", email="mukisa@school.ac.ug", reg_number="21/U/1001"),
    StudentCreate(name="Aisha Nakato",  email="aisha@school.ac.ug",  reg_number="21/U/1002"),
    StudentCreate(name="Brian Okello",  email="brian@school.ac.ug",  reg_number="21/U/1003"),
]


def main() -> None:
    db = SessionLocal()
    try:
        added = 0
        for student in SAMPLE_STUDENTS:
            # Skip anyone already in the database so re-running is safe.
            if crud.student.get_by_email(db, student.email):
                print(f"  skipped (already exists): {student.email}")
                continue
            crud.student.create(db, student)
            added += 1
            print(f"  added: {student.name} ({student.reg_number})")
        print(f"\nDone. {added} new student(s) added.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
