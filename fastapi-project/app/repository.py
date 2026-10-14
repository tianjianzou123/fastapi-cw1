"""Thread-safe in-memory storage for the Task Manager API."""

from datetime import datetime, timezone
from threading import RLock

from .models import TaskCreate, TaskRead, TaskReplace, TaskStatus


class TaskNotFoundError(LookupError):
    """Raised when a task identifier does not exist."""


class TaskRepository:
    """Store task records in memory for a small teaching example."""

    def __init__(self) -> None:
        self._tasks: dict[int, TaskRead] = {}
        self._next_id = 1
        self._lock = RLock()

    def list_all(
        self,
        *,
        status: TaskStatus | None = None,
        priority: int | None = None,
    ) -> list[TaskRead]:
        """Return tasks in identifier order with optional filters."""

        with self._lock:
            tasks = sorted(self._tasks.values(), key=lambda task: task.id)
            if status is not None:
                tasks = [task for task in tasks if task.status == status]
            if priority is not None:
                tasks = [task for task in tasks if task.priority == priority]
            return [task.model_copy(deep=True) for task in tasks]

    def create(self, data: TaskCreate) -> TaskRead:
        """Create and store a new task."""

        with self._lock:
            now = _utc_now()
            task = TaskRead(
                id=self._next_id,
                created_at=now,
                updated_at=now,
                **data.model_dump(),
            )
            self._tasks[task.id] = task
            self._next_id += 1
            return task.model_copy(deep=True)

    def get(self, task_id: int) -> TaskRead:
        """Return one task or raise TaskNotFoundError."""

        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(task_id)
            return task.model_copy(deep=True)

    def replace(self, task_id: int, data: TaskReplace) -> TaskRead:
        """Replace all editable fields of an existing task."""

        with self._lock:
            current = self._tasks.get(task_id)
            if current is None:
                raise TaskNotFoundError(task_id)
            updated = TaskRead(
                id=current.id,
                created_at=current.created_at,
                updated_at=_utc_now(),
                **data.model_dump(),
            )
            self._tasks[task_id] = updated
            return updated.model_copy(deep=True)

    def delete(self, task_id: int) -> None:
        """Delete one task or raise TaskNotFoundError."""

        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFoundError(task_id)
            del self._tasks[task_id]


def _utc_now() -> datetime:
    """Return a timezone-aware timestamp."""

    return datetime.now(timezone.utc)

