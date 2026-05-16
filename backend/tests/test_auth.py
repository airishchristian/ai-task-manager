# tests/test_auth.py
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "newpass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "newuser@example.com"
    assert "password" not in data  # never leak password


def test_register_duplicate_email(client: TestClient, test_user):
    response = client.post(
        "/auth/register",
        json={
            "name": "Duplicate User",
            "email": test_user["email"],  # same email as fixture
            "password": "anotherpass123",
        },
    )
    assert response.status_code == 400


def test_login_success(client: TestClient, test_user):
    response = client.post(
        "/auth/login",
        json={                             
            "email": test_user["email"],
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],  
            "password": "wrongpass",
        },
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        json={
            "email": "ghost@example.com",
            "password": "doesnotexist",
        },
    )
    assert response.status_code == 401