"""
schemas/student.py
------------------
SCHEMAS define the shape of data going IN and OUT of the API (Pydantic).

Why several classes for one thing? Because different situations need
different fields:

  * StudentCreate — what the client must SEND to create a student
                    (no id — the database assigns it).
  * StudentUpdate — fields allowed when editing (all optional).
  * StudentRead   — what the API SENDS BACK (includes the id).

Keeping these separate from the database model means you can change your
storage without changing your public API, and vice versa.
"""

from pydantic import BaseModel, EmailStr, ConfigDict


# Fields shared by create & read live in a common base to avoid repetition.
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    reg_number: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    reg_number: str | None = None


class StudentRead(StudentBase):
    id: int

    # from_attributes=True lets Pydantic read data straight off a
    # SQLAlchemy object (student.name) instead of a dict (student["name"]).
    model_config = ConfigDict(from_attributes=True)
