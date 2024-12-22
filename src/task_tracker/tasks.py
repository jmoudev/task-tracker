import os

import task_tracker.utils as utils


class Task:
    def __init__(
        self,
        _id,
        description,
        status="todo",
        created_at=utils.get_iso_datetime(),
        updated_at=utils.get_iso_datetime(),
    ):
        self.id = _id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            task_dict["id"],
            task_dict.get("description"),
            task_dict.get("status"),
            task_dict.get("createdAt"),
            task_dict.get("updatedAt"),
        )

    def update(self, update_field, update_value):
        setattr(self, update_field, update_value)
        self.updated_at = utils.get_iso_datetime()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }


class TasksFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        if not os.path.isfile(filepath):
            tasks_obj = {}
        else:
            tasks_obj = utils.read_json(filepath)
        self.metadata = tasks_obj.get("metadata", {})
        self.tasks = tasks_obj.get("tasks", {})

    def _get_task_by_id(self, _id):
        return Task.from_dict(self.tasks[str(_id)])

    def add_task(self, description):
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

    def update_task_description(self, _id, description):
        return self._update_task(_id, "description", description)

    def update_task_status(self, _id, status):
        return self._update_task(_id, "status", status)

    def delete_task(self, _id):
        del self.tasks[str(_id)]
        self._save()
        return f"Task deleted successfully (ID: {_id})"

    def list_tasks_by_status(self, status):
        return [
            task
            for task in self.tasks.values()
            if not status or task["status"] == status
        ]

    def _save(self):
        tasks_obj = {"metadata": self.metadata, "tasks": self.tasks}
        utils.write_json(self.filepath, tasks_obj)
