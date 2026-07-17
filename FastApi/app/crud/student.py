"""
crud/student.py
---------------
CRUD = Create, Read, Update, Delete.

This layer holds the actual DATABASE QUERIES for students. The endpoints
(routes) call these functions instead of writing SQL themselves.

Why bother? So the same query logic can be reused (by routes, by tests,
by other code) and lives in ONE place. If a query needs fixing, you fix
it here, not in several different endpoints.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def get(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def get_by_email(db: Session, email: str) -> Student | None:
    return db.scalar(select(Student).where(Student.email == email))


def get_by_reg_number(db: Session, reg_number: str) -> Student | None:
    return db.scalar(select(Student).where(Student.reg_number == reg_number))


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[Student]:
    return list(db.scalars(select(Student).offset(skip).limit(limit)))


def create(db: Session, data: StudentCreate) -> Student:
    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)  # reload so we get the DB-assigned id
    return student


def update(db: Session, student: Student, data: StudentUpdate) -> Student:
    # exclude_unset=True => only overwrite the fields the client actually sent
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def remove(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()
