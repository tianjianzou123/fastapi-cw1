"""Application factory and HTTP routes for the Task Manager API."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query, Response, status

from .models import (
    ApiMessage,
    HealthResponse,
    TaskCreate,
    TaskRead,
    TaskReplace,
    TaskStatus,
)
from .repository import TaskNotFoundError, TaskRepository


def create_app(repository: TaskRepository | None = None) -> FastAPI:
    """Create an application with an injectable task repository."""

    task_repository = repository or TaskRepository()
    application = FastAPI(
        title="FastAPI Task Manager",
        summary="A small REST API for managing presentation tasks.",
        description=(
            "A teaching example that demonstrates CRUD routes, Pydantic validation, "
            "query parameters, HTTP status codes, and generated OpenAPI documentation."
        ),
        version="1.0.0",
        contact={"name": "COMP10020 FastAPI Group"},
        license_info={"name": "MIT"},
        openapi_tags=[
            {"name": "meta", "description": "API information and service health."},
            {"name": "tasks", "description": "Create, read, replace, and delete tasks."},
        ],
    )

    @application.get("/", response_model=ApiMessage, tags=["meta"])
    def read_root() -> ApiMessage:
        """Point new users to the generated API documentation."""

        return ApiMessage(
            message="FastAPI Task Manager is running.",
            docs_url="/docs",
            redoc_url="/redoc",
        )

    @application.get("/health", response_model=HealthResponse, tags=["meta"])
    def read_health() -> HealthResponse:
        """Provide a simple health check for clients and hosting platforms."""

        return HealthResponse(status="ok")

    @application.get("/tasks", response_model=list[TaskRead], tags=["tasks"])
    def list_tasks(
        task_status: Annotated[
            TaskStatus | None,
            Query(alias="status", description="Return only tasks in this workflow state."),
        ] = None,
        priority: Annotated[
            int | None,
            Query(ge=1, le=5, description="Return only tasks with this priority."),
        ] = None,
    ) -> list[TaskRead]:
        """List tasks, optionally filtering by status and priority."""

        return task_repository.list_all(status=task_status, priority=priority)

    @application.post(
        "/tasks",
        response_model=TaskRead,
        status_code=status.HTTP_201_CREATED,
        tags=["tasks"],
    )
    def create_task(data: TaskCreate) -> TaskRead:
        """Create a task after Pydantic validates the request body."""

        return task_repository.create(data)

    @application.get("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
    def read_task(
        task_id: Annotated[int, Path(gt=0, description="Numeric task identifier.")],
    ) -> TaskRead:
        """Return one task by identifier."""

        try:
            return task_repository.get(task_id)
        except TaskNotFoundError as error:
            raise _not_found(task_id) from error

    @application.put("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
    def replace_task(
        task_id: Annotated[int, Path(gt=0, description="Numeric task identifier.")],
        data: TaskReplace,
    ) -> TaskRead:
        """Replace all editable fields of a task."""

        try:
            return task_repository.replace(task_id, data)
        except TaskNotFoundError as error:
            raise _not_found(task_id) from error

    @application.delete(
        "/tasks/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        tags=["tasks"],
    )
    def delete_task(
        task_id: Annotated[int, Path(gt=0, description="Numeric task identifier.")],
    ) -> Response:
        """Delete a task and return an empty 204 response."""

        try:
            task_repository.delete(task_id)
        except TaskNotFoundError as error:
            raise _not_found(task_id) from error
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return application


def _not_found(task_id: int) -> HTTPException:
    """Build the consistent 404 response used by task endpoints."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} was not found.",
    )


app = create_app()

