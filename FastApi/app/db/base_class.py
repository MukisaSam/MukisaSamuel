"""
db/base_class.py
----------------
Defines "Base" — the parent class that every database model inherits from.

SQLAlchemy uses this single Base to keep a registry of all your tables
(its ".metadata"). That registry is what lets us create every table at
once, and what Alembic reads to auto-generate migrations.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
