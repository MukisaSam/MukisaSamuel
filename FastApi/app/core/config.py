"""
core/config.py
--------------
Central place for ALL application settings.

Instead of scattering magic values (like the database URL) across the
code, we collect them here. Pydantic's BaseSettings reads them from
environment variables / the .env file automatically, and validates types.

Rule of thumb: anything that changes between your laptop, the test
server, and production belongs here — never hard-coded in the middle
of your logic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Tells Pydantic to load variables from a file named ".env"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Student Information API"
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    # SQLite keeps the whole database in a single file (students.db) so the
    # demo runs with zero setup. In production you'd point this at Postgres.
    DATABASE_URL: str = "sqlite:///./students.db"


# One shared instance the rest of the app imports:  from app.core.config import settings
settings = Settings()
