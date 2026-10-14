"""Automated API tests for the FastAPI Task Manager."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import TaskRepository


@pytest.fixture
def client() -> TestClient:
    """Give each test a new application and empty in-memory repository."""

    with TestClient(create_app(TaskRepository())) as test_client:
        yield test_client


def create_sample_task(client: TestClient, **overrides: object) -> dict[str, object]:
    """Create one valid task and return its JSON response."""

    payload: dict[str, object] = {
        "title": "Prepare the FastAPI demo",
        "description": "Test the API before class.",
        "status": "todo",
        "priority": 4,
    }
    payload.update(overrides)
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_root_health_and_generated_documentation(client: TestClient) -> None:
    root = client.get("/")
    health = client.get("/health")
    docs = client.get("/docs")
    schema = client.get("/openapi.json")

    assert root.status_code == 200
    assert root.json()["docs_url"] == "/docs"
    assert health.json() == {"status": "ok"}
    assert docs.status_code == 200
    assert "swagger-ui" in docs.text.lower()
    assert schema.status_code == 200
    assert "/tasks" in schema.json()["paths"]
    assert "/tasks/{task_id}" in schema.json()["paths"]


def test_create_and_list_tasks(client: TestClient) -> None:
    created = create_sample_task(client)

    assert created["id"] == 1
    assert created["title"] == "Prepare the FastAPI demo"
    assert created["created_at"] == created["updated_at"]

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [created]


def test_get_one_task_and_missing_task(client: TestClient) -> None:
    created = create_sample_task(client)

    found = client.get(f"/tasks/{created['id']}")
    missing = client.get("/tasks/999")

    assert found.status_code == 200
    assert found.json() == created
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Task 999 was not found."}


def test_validation_rejects_blank_title_and_invalid_priority(client: TestClient) -> None:
    blank_title = client.post(
        "/tasks",
        json={"title": "   ", "priority": 3},
    )
    invalid_priority = client.post(
        "/tasks",
        json={"title": "Valid title", "priority": 6},
    )

    assert blank_title.status_code == 422
    assert invalid_priority.status_code == 422
    assert client.get("/tasks").json() == []


def test_replace_task_preserves_identity_and_created_time(client: TestClient) -> None:
    created = create_sample_task(client)
    replacement = {
        "title": "Deliver the FastAPI presentation",
        "description": None,
        "status": "done",
        "priority": 5,
    }

    response = client.put(f"/tasks/{created['id']}", json=replacement)

    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == created["id"]
    assert updated["created_at"] == created["created_at"]
    assert updated["updated_at"] >= created["updated_at"]
    assert updated["title"] == replacement["title"]
    assert updated["description"] is None
    assert updated["status"] == "done"
    assert updated["priority"] == 5


def test_replace_missing_task_returns_404(client: TestClient) -> None:
    response = client.put(
        "/tasks/100",
        json={"title": "Missing", "status": "todo", "priority": 1},
    )

    assert response.status_code == 404


def test_delete_task_returns_204_and_removes_record(client: TestClient) -> None:
    created = create_sample_task(client)

    deleted = client.delete(f"/tasks/{created['id']}")
    missing = client.get(f"/tasks/{created['id']}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert missing.status_code == 404


def test_list_filters_by_status_and_priority(client: TestClient) -> None:
    create_sample_task(client, title="First", status="todo", priority=2)
    second = create_sample_task(client, title="Second", status="done", priority=5)
    create_sample_task(client, title="Third", status="done", priority=2)

    done_tasks = client.get("/tasks", params={"status": "done"})
    urgent_done_tasks = client.get(
        "/tasks",
        params={"status": "done", "priority": 5},
    )
    invalid_filter = client.get("/tasks", params={"priority": 0})

    assert done_tasks.status_code == 200
    assert [task["title"] for task in done_tasks.json()] == ["Second", "Third"]
    assert urgent_done_tasks.json() == [second]
    assert invalid_filter.status_code == 422

