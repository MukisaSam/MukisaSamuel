"""
api/v1/router.py
----------------
Combines every endpoint file into ONE router for version 1 of the API.

Each endpoint file gets a URL prefix and a tag (tags group them in /docs).
main.py then includes this single api_router — so main.py stays tidy no
matter how many endpoint files you add.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import students, reports

api_router = APIRouter()

api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
