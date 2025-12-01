from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from dz9.main import StudentRepo
from dz11.auth import get_current_user
from dz11.main import app, student_repo_depends


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=StudentRepo)
    return repo


@pytest.fixture
def client(mock_repo):
    def override_repo():
        yield mock_repo


    FastAPICache.init(InMemoryBackend())

    app.dependency_overrides[student_repo_depends] = override_repo

    app.dependency_overrides[get_current_user] = lambda: {"id": 1}

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# -------------------------------------------------------------
# GET /
# -------------------------------------------------------------
def test_get_students(client, mock_repo):
    mock_repo.select_users.return_value = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "faculty": "Math",
            "course": "1",
            "mark": 5,
        }
    ]

    response = client.get("/", params={"first_name": "John"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "faculty": "Math",
            "course": "1",
            "mark": 5,
        }
    ]

    mock_repo.select_users.assert_called_once_with({"first_name": "John"})


# -------------------------------------------------------------
# POST /
# -------------------------------------------------------------
def test_create_student(client, mock_repo):
    mock_repo.insert_user.return_value = {
        "id": 10,
        "first_name": "Ann",
        "last_name": "Lee",
        "faculty": "CS",
        "course": "2",
        "mark": 4,
    }

    payload = {
        "first_name": "Ann",
        "last_name": "Lee",
        "faculty": "CS",
        "course": "2",
        "mark": 4,
    }

    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 10

    mock_repo.insert_user.assert_called_once_with(payload)


# -------------------------------------------------------------
# PUT /
# -------------------------------------------------------------
def test_update_student(client, mock_repo):
    payload = {
        "id": 3,
        "first_name": "Bob",
        "last_name": "Ross",
        "faculty": "Art",
        "course": "3",
        "mark": 5,
    }

    response = client.put("/", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

    mock_repo.update_user.assert_called_once_with(3, payload)


# -------------------------------------------------------------
# DELETE /{id}
# -------------------------------------------------------------
def test_delete_student(client, mock_repo):
    response = client.delete("/5")
    assert response.status_code == 200

    mock_repo.delete_user.assert_called_once_with(5)
