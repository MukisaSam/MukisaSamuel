"""
api/v1/endpoints/reports.py
---------------------------
A tiny endpoint that shows the SERVICES layer in action: it just asks the
reporting service for a summary and returns it. No logic lives here.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services import reporting

router = APIRouter()


@router.get("/summary")
def students_summary(db: Session = Depends(get_db)):
    return reporting.build_summary(db)
