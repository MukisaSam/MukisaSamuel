"""
api/v1/endpoints/students.py
----------------------------
The main resource of the demo: full CRUD for students.

Each function is an ENDPOINT. The decorator says which HTTP method and
URL path it answers:
    GET    -> read data
    POST   -> create data
    PUT    -> update data
    DELETE -> remove data

Notice how thin these functions are: they receive the request, call the
crud/ layer, and return the result. All the database work lives in crud/.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate

router = APIRouter()


@router.get("/", response_model=list[StudentRead])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.student.get_multi(db, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.student.get(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    if crud.student.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if crud.student.get_by_reg_number(db, data.reg_number):
        raise HTTPException(status_code=400, detail="Reg number already exists")
    return crud.student.create(db, data)


@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = crud.student.get(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.student.update(db, student, data)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.student.get(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    crud.student.remove(db, student)
