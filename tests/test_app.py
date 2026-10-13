
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_list_students(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_add_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Aarav Patil",
            "email": "aarav@example.com",
            "course": "Information Technology"
        }
    )

    assert response.status_code == 201
    assert response.json["name"] == "Aarav Patil"
    assert response.json["id"] > 0


def test_reject_missing_fields(client):
    response = client.post(
        "/students",
        json={"name": "Aarav Patil"}
    )

    assert response.status_code == 400
    assert "error" in response.json


def test_reject_non_json_request(client):
    response = client.post("/students", data="invalid")
    assert response.status_code == 400
