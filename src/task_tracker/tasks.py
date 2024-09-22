from __future__ import annotations

import os
from typing import TypedDict

import task_tracker.utils as utils


Metadata = dict[str, int]
TaskDict = TypedDict(
    "TaskDict",
    {"id": int, "description": str, "status": str, "createdAt": str, "updatedAt": str},
    total=False,
)
Tasks = dict[str, TaskDict]
TasksJson = TypedDict("TasksJson", {"metadata": Metadata, "tasks": Tasks}, total=False)


class TaskKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Task:
    """Class representing a single task.

    Attributes:
        id: Unique integer id.
        description: Task description string.
        status: Task status string.
        createdAt: Isoformat timestamp string at task creation.
        updatedAt: Isoformat timestamp string at task last update.
    """

    def __init__(
        self,
        _id: int,
        description: str,
        status: str = "todo",
        created_at: str = utils.get_iso_datetime(),
        updated_at: str = utils.get_iso_datetime(),
    ):
        self.id = _id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, task_dict: TaskDict) -> Task:
        return cls(
            task_dict["id"],
            task_dict["description"],
            task_dict["status"],
            task_dict["createdAt"],
            task_dict["updatedAt"],
        )

    def update(self, update_field, update_value):
        setattr(self, update_field, update_value)
        self.updated_at = utils.get_iso_datetime()

    def to_dict(self) -> TaskDict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }


class TasksFile:
    """Class for reading / modifying the task json file.

    Attributes:
        filepath: Filepath string to tasks json file.
        metadata: Metadata dict related to task operations.
        tasks: Tasks mapping containing individual task dicts.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.isfile(filepath):
            tasks_json: TasksJson = {}
        else:
            tasks_json = utils.read_json(filepath)
        self.metadata: Metadata = tasks_json.get("metadata", {})
        self.tasks: Tasks = tasks_json.get("tasks", {})

    def _get_task_by_id(self, _id: int) -> Task | TaskKeyError:
        try:
            return Task.from_dict(self.tasks[str(_id)])
        except KeyError:
            raise TaskKeyError(f"Task of ID: {_id} does not exist")

    def add_task(self, description: str) -> TaskDict:
        """Add a task to the tasks file."""
        task_id = self.metadata.get("task_counter", 0) + 1
        task_dict = Task(task_id, description).to_dict()
        self.tasks[str(task_id)] = task_dict
        self.metadata["task_counter"] = task_id
        self._save()
        return task_dict

    def _update_task(self, _id, update_field, update_value):
        task = self._get_task_by_id(_id)
        task.update(update_field, update_value)
        updated_task_dict = task.to_dict()
        self.tasks[str(_id)] = updated_task_dict
        self._save()
        return updated_task_dict

    def update_task_description(self, _id: int, description: str) -> TaskDict:
        """Update a tasks description in the tasks file."""
        return self._update_task(_id, "description", description)

    def update_task_status(self, _id: int, status: str) -> TaskDict:
        """Update a tasks status in the tasks file."""
        return self._update_task(_id, "status", status)

    def delete_task(self, _id: int) -> str | TaskKeyError:
        """Delete a task from the task file."""
        try:
            del self.tasks[str(_id)]
        except KeyError:
            raise TaskKeyError(
                f"Task delete unsuccessful. Task of ID: {_id} does not exist"
            )
        self._save()
        return f"Task deleted successfully (ID: {_id})"

    def list_tasks_by_status(self, status: str | None) -> list[TaskDict]:
        """List tasks in the task file by status or with falsy status for all."""
        return [
            task
            for task in self.tasks.values()
            if not status or task["status"] == status
        ]

    def _save(self):
        tasks_obj = {"metadata": self.metadata, "tasks": self.tasks}
        utils.write_json(self.filepath, tasks_obj)
