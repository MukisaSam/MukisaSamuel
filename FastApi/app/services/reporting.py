"""
services/reporting.py
---------------------
The SERVICES layer holds "business logic" — anything that is more than a
simple database read/write and doesn't belong to a single endpoint.

Here it is a small summary about the students. An endpoint can call this
without caring HOW the numbers are worked out. If the rules change, you
edit them here, in one place.
"""

from sqlalchemy.orm import Session

from app import crud


def build_summary(db: Session) -> dict:
    """Return a small summary of all students."""
    students = crud.student.get_multi(db, limit=1000)
    return {
        "total_students": len(students),
    }
