import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_login_success(client):
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    r = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401


def test_protected_without_token(client):
    r = client.get("/api/data")
    assert r.status_code == 401


def test_protected_with_token(client):
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = r.json()["access_token"]
    r = client.get("/api/data", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_post_sanitizes_xss(client):
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = r.json()["access_token"]
    r = client.post(
        "/api/posts",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "<script>alert(1)</script>", "content": "hello <b>world</b>"},
    )
    assert r.status_code == 201
    body = r.json()
    assert "<script>" not in body["title"]
    assert "&lt;script&gt;" in body["title"]