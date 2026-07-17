"""
main.py
-------
THE ENTRY POINT. The server runs this first.

It is deliberately SHORT. All it does is assemble the pieces that live in
the other folders:
  1. create the FastAPI() application,
  2. include the versioned API router (all /api/v1/... endpoints),
  3. serve the single HTML page that displays students.

The database tables are NOT created here — that is Alembic's job:
    alembic upgrade head          (create/upgrade the tables)
    python -m scripts.seed_data   (add the demo students)

Run the app with:   uvicorn app.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.services import reporting

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A full-structure FastAPI demo for introducing FastAPI.",
    version="1.0.0",
)

# Serve the CSS from /static, and register the templates folder.
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Plug in every /api/v1/... endpoint with one line.
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The single web page. Reads students + a summary and renders them."""
    db = SessionLocal()
    try:
        from app import crud

        students = crud.student.get_multi(db, limit=1000)
        summary = reporting.build_summary(db)
    finally:
        db.close()

    # Modern Starlette signature: request first, then template name, then context.
    return templates.TemplateResponse(
        request,
        "index.html",
        {"students": students, "summary": summary},
    )
