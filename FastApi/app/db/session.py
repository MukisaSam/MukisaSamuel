"""
db/session.py
-------------
Creates the connection to the database.

  * engine        — the low-level connection pool to the database.
  * SessionLocal  — a factory that hands out a "Session" (one conversation
                    with the DB). Each request gets its own session and
                    closes it when done (see api/deps.py -> get_db).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# check_same_thread=False is only needed for SQLite + FastAPI.
# Remove it if you switch to Postgres/MySQL.
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
