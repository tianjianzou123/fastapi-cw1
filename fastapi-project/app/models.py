"""Pydantic models used by the Task Manager API."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    """Allowed workflow states for a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskData(BaseModel):
    """Fields supplied by a client when creating or replacing a task."""

    title: str = Field(
        min_length=1,
        max_length=120,
        examples=["Prepare the FastAPI demo"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        examples=["Test every endpoint before the group presentation."],
    )
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: int = Field(default=3, ge=1, le=5)

    @field_validator("title")
    @classmethod
    def title_must_contain_text(cls, value: str) -> str:
        """Trim the title and reject values made only of whitespace."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must contain at least one visible character")
        return cleaned

    @field_validator("description")
    @classmethod
    def normalise_description(cls, value: str | None) -> str | None:
        """Trim an optional description and store an empty value as null."""

        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class TaskCreate(TaskData):
    """Request body for POST /tasks."""


class TaskReplace(TaskData):
    """Request body for PUT /tasks/{task_id}."""


class TaskRead(TaskData):
    """Task representation returned to API clients."""

    id: int
    created_at: datetime
    updated_at: datetime


class ApiMessage(BaseModel):
    """Small response model used for API metadata."""

    message: str
    docs_url: str
    redoc_url: str


class HealthResponse(BaseModel):
    """Response model for the health endpoint."""

    status: str

