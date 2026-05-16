# tests/test_tasks.py
from fastapi.testclient import TestClient


def test_create_task(client: TestClient, auth_headers: dict):
    response = client.post(
        "/tasks/",
        json={"title": "My First Task", "description": "Do something important"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Task"
    assert data["status"] == "pending"  # default status


def test_create_task_unauthenticated(client: TestClient):
    response = client.post(
        "/tasks/",
        json={"title": "Unauthorized Task"},
    )
    assert response.status_code in (401, 403)


def test_get_all_tasks(client: TestClient, auth_headers: dict):
    # Create a task first
    client.post(
        "/tasks/",
        json={"title": "Task for listing"},
        headers=auth_headers,
    )
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_task_by_id(client: TestClient, auth_headers: dict):
    # Create a task
    create_resp = client.post(
        "/tasks/",
        json={"title": "Task to fetch"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]

    # Fetch by ID
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task to fetch"


def test_get_nonexistent_task(client: TestClient, auth_headers: dict):
    response = client.get("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client: TestClient, auth_headers: dict):
    # Create a task
    create_resp = client.post(
        "/tasks/",
        json={"title": "Task to update"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]

    # Update status
    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "completed"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


def test_delete_task(client: TestClient, auth_headers: dict):
    # Create a task
    create_resp = client.post(
        "/tasks/",
        json={"title": "Task to delete"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]

    # Delete it
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Confirm it's gone
    get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404
