# Expose the submodule so callers can write:  crud.student.create(...)
from app.crud import student  # noqa: F401
