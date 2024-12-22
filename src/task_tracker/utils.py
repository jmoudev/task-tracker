import datetime
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_tracker.tasks import TasksJson


def read_json(
    json_filepath: str,
) -> "TasksJson":
    with open(json_filepath) as json_fp:
        json_data = json.load(json_fp)
    return json_data


def write_json(json_filepath: str, json_data) -> None:
    with open(json_filepath, "w") as json_fp:
        json.dump(json_data, json_fp, indent=4)


def create_tasks_json(json_filepath: str) -> None:
    tasks_json = {"metadata": {"num_tasks": 0}, "tasks": {}}
    write_json(json_filepath, tasks_json)


def get_iso_datetime() -> str:
    return datetime.datetime.now().isoformat()
