"""
api/deps.py
-----------
Shared DEPENDENCIES.

A "dependency" in FastAPI is a function that prepares something an
endpoint needs, and is injected automatically via Depends(...).

The classic example is get_db: it opens a database session, hands it to
the endpoint, and guarantees the session is closed afterwards. Endpoints
just write  `db: Session = Depends(get_db)`  and FastAPI does the rest,
so this boilerplate lives in ONE place instead of every route.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session and guarantee it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
