import argparse
import datetime
import json
import os
import pprint


JSON_FILENAME = "tasks.json"
JSON_FILEPATH = os.path.join(os.curdir, JSON_FILENAME)


def read_json(json_filepath):
    with open(json_filepath) as json_fp:
        _json = json.load(json_fp)
    return _json


def write_json(json_filepath, json_data):
    with open(json_filepath, "w") as json_fp:
        json.dump(json_data, json_fp, indent=4)


def create_tasks_json(json_filepath):
    tasks_json = {"metadata": {"num_tasks": 0}, "tasks": {}}
    write_json(json_filepath, tasks_json)


def get_iso_datetime():
    return datetime.datetime.now().isoformat()


def add_task(json_filepath, description):
    tasks_json = read_json(json_filepath)
    _id = tasks_json["metadata"]["num_tasks"] + 1
    created_timestamp = datetime.datetime.now().isoformat()
    tasks_json["metadata"]["num_tasks"] += 1
    # json writes dict keys as str
    task = {
        "id": _id,
        "description": description,
        "status": "todo",
        "createdAt": created_timestamp,
        "updatedAt": created_timestamp,
    }
    tasks_json["tasks"][str(_id)] = task
    write_json(json_filepath, tasks_json)
    return task


def update_task(json_filepath, _id, description):
    tasks_json = read_json(json_filepath)
    task = tasks_json["tasks"][str(_id)]
    task["description"] = description
    task["updatedAt"] = get_iso_datetime()
    write_json(json_filepath, tasks_json)
    return task


def delete_task(json_filepath, _id):
    tasks_json = read_json(json_filepath)
    del tasks_json["tasks"][str(_id)]
    write_json(json_filepath, tasks_json)
    return f"Task of id {_id} deleted from {JSON_FILENAME}."


def mark_task_status(json_filepath, _id, status):
    tasks_json = read_json(json_filepath)
    task = tasks_json["tasks"][str(_id)]
    task["status"] = status
    task["updatedAt"] = get_iso_datetime()
    write_json(json_filepath, tasks_json)
    return task


def list_tasks(json_filepath, status):
    tasks_json = read_json(json_filepath)
    tasks_list = tasks_json["tasks"]
    if status:
        tasks_list = [task for task in tasks_list if task["status"] == status]
    return tasks_list


def main():
    if not os.path.isfile(JSON_FILEPATH):
        create_tasks_json(JSON_FILEPATH)

    parser = argparse.ArgumentParser(
        prog="task-cli", description="To-do list cli application"
    )
    parser.set_defaults(which=None)
    subparsers = parser.add_subparsers()

    task_adder = subparsers.add_parser("add")
    task_adder.add_argument("description", type=str)
    task_adder.set_defaults(which="add")

    task_updater = subparsers.add_parser("update")
    task_updater.add_argument("id", type=int)
    task_updater.add_argument("description", type=str)
    task_updater.set_defaults(which="update")

    task_deleter = subparsers.add_parser("delete")
    task_deleter.add_argument("id", type=int)
    task_deleter.set_defaults(which="delete")

    task_mark_in_progress = subparsers.add_parser("mark-in-progress")
    task_mark_in_progress.add_argument("id", type=int)
    task_mark_in_progress.set_defaults(which="mark-in-progress")

    task_mark_done = subparsers.add_parser("mark-done")
    task_mark_done.add_argument("id", type=int)
    task_mark_done.set_defaults(which="mark-done")

    task_lister = subparsers.add_parser("list")
    task_lister.add_argument("status", nargs="?", type=str)
    task_lister.set_defaults(which="list")

    args = parser.parse_args()

    match args.which:
        case "add":
            pprint.pprint(add_task(JSON_FILEPATH, args.description))
        case "update":
            pprint.pprint(update_task(JSON_FILEPATH, args.id, args.description))
        case "delete":
            print(delete_task(JSON_FILEPATH, args.id))
        case "mark-in-progress":
            pprint.pprint(mark_task_status(JSON_FILEPATH, args.id, "in-progress"))
        case "mark-done":
            pprint.pprint(mark_task_status(JSON_FILEPATH, args.id, "done"))
        case "list":
            pprint.pprint(list_tasks(JSON_FILEPATH, args.status))
        case None:
            parser.print_help()


if __name__ == "__main__":
    main()
