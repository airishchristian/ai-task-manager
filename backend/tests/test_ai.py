# tests/test_ai.py
from fastapi.testclient import TestClient


def test_breakdown_task(client: TestClient, auth_headers: dict):
    response = client.post(
        "/ai/breakdown",
        json={"task_title": "Build a website"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "subtasks" in data
    assert isinstance(data["subtasks"], list)
    assert len(data["subtasks"]) > 0
    assert all(isinstance(item, str) for item in data["subtasks"])


def test_breakdown_unauthenticated(client: TestClient):
    response = client.post(
        "/ai/breakdown",
        json={"task_title": "Unauthorized breakdown"},
    )
    assert response.status_code in (401, 403)


def test_prioritize_task(client: TestClient, auth_headers: dict):
    response = client.post(
        "/ai/prioritize",
        json={"task_title": "Submit tax return", "due_date": "2025-04-15"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "priority" in data
    assert data["priority"] in ["low", "medium", "high"]
    assert "reasoning" in data
    assert isinstance(data["reasoning"], str)
    assert len(data["reasoning"]) > 0
