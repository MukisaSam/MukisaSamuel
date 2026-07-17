"""
tests/test_students.py
----------------------
Tests for the student endpoints. Each test uses the `client` fixture,
which talks to a throwaway test database (see conftest.py).

Run them with:   pytest
"""

from app.core.config import settings

BASE = f"{settings.API_V1_PREFIX}/students"


def test_list_is_empty_at_first(client):
    response = client.get(f"{BASE}/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_read_student(client):
    payload = {
        "name": "Jane Doe",
        "email": "jane@school.ac.ug",
        "reg_number": "22/U/2001",
    }
    # Create
    created = client.post(f"{BASE}/", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "Jane Doe"
    assert "id" in body  # the database assigned an id

    # Read it back by id
    student_id = body["id"]
    fetched = client.get(f"{BASE}/{student_id}")
    assert fetched.status_code == 200
    assert fetched.json()["reg_number"] == "22/U/2001"


def test_duplicate_email_is_rejected(client):
    payload = {"name": "A", "email": "dup@school.ac.ug", "reg_number": "22/U/3001"}
    client.post(f"{BASE}/", json=payload)

    payload2 = {"name": "B", "email": "dup@school.ac.ug", "reg_number": "22/U/3002"}
    response = client.post(f"{BASE}/", json=payload2)
    assert response.status_code == 400


def test_missing_student_returns_404(client):
    response = client.get(f"{BASE}/999")
    assert response.status_code == 404
