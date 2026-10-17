import pytest
from app import create_app

@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "test", "DATABASE": str(tmp_path / "test.db")})
    with app.test_client() as c:
        yield c

def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"StudentHub" in r.data

def test_directory(client):
    assert client.get("/students").status_code == 200

def test_add_student(client):
    r = client.post("/students/add", data={"name":"Aditi Sharma","email":"aditi@example.com","course":"Information Technology"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Aditi Sharma" in r.data

def test_duplicate_email_rejected(client):
    data = {"name":"Aditi Sharma","email":"aditi@example.com","course":"Information Technology"}
    client.post("/students/add", data=data)
    r = client.post("/students/add", data={**data, "name":"Other Student"})
    assert b"already registered" in r.data

def test_edit_and_delete(client):
    client.post("/students/add", data={"name":"Aditi Sharma","email":"aditi@example.com","course":"Information Technology"})
    r = client.post("/students/1/edit", data={"name":"Aditi Patil","email":"aditi@example.com","course":"Cyber Security"}, follow_redirects=True)
    assert b"Aditi Patil" in r.data
    r = client.post("/students/1/delete", follow_redirects=True)
    assert b"No students found" in r.data

def test_api_requires_json(client):
    assert client.post("/api/students", data="name=Example").status_code == 400

def test_api_add_student(client):
    r = client.post("/api/students", json={"name":"Ravi Patil","email":"ravi@example.com","course":"Data Science"})
    assert r.status_code == 201
