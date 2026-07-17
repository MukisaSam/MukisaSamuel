"""
models/student.py
-----------------
A MODEL describes a real database TABLE using SQLAlchemy.

This "Student" class becomes a table called "students". Each attribute
(Mapped[...]) becomes a column, and every row is one student record.

Do not confuse MODELS with SCHEMAS:
  * models/  = database tables (SQLAlchemy)        -> how data is STORED
  * schemas/ = request/response shapes (Pydantic)  -> how data TRAVELS
"""

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    reg_number: Mapped[str] = mapped_column(unique=True, index=True)