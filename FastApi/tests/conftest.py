"""
tests/conftest.py
-----------------
Pytest FIXTURES — reusable setup shared by all tests.

The key idea: tests must NOT touch your real database. So we:
  1. spin up a separate, throwaway SQLite database just for the tests,
  2. override the app's get_db dependency to use it, and
  3. hand each test a ready-to-use TestClient to make fake HTTP requests.

Because get_db is a dependency, swapping it out for tests is trivial —
that is one of the big payoffs of the dependency-injection structure.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base_class import Base
from app.main import app

# A separate in-memory-ish test database (a local file we delete freely).
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    # Fresh, empty tables for every test.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Tell FastAPI: during tests, use the test database instead.
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
