import argparse
import datetime
import json
import os


JSON_FILENAME = "tasks.json"
JSON_FILEPATH = os.path.join(os.curdir, JSON_FILENAME)


def read_json(json_filepath):
    with open(json_filepath) as json_fp:
        _json = json.load(json_fp)
    return _json


def write_json(json_filepath, json_data):
    with open(json_filepath, "w") as json_fp:
        json.dump(json_data, json_fp)
    return


def create_tasks_json(json_filepath):
    tasks_json = {"metadata": {"num_tasks": 0}, "tasks": []}
    write_json(json_filepath, tasks_json)
    return


def add_task(json_filepath, description):
    tasks_json = read_json(json_filepath)
    _id = tasks_json["metadata"]["num_tasks"] + 1
    created_timestamp = datetime.datetime.now().isoformat()
    tasks_json["metadata"]["num_tasks"] = tasks_json["metadata"]["num_tasks"] + 1
    tasks_json["tasks"].append(
        {
            "id": _id,
            "description": description,
            "status": "todo",
            "createdAt": created_timestamp,
            "updatedAt": created_timestamp,
        }
    )
    write_json(json_filepath, tasks_json)
    return


def update_task(json_filepath, _id, description):
    tasks_json = read_json(json_filepath)
    for task in tasks_json["tasks"]:
        if task["id"] == _id:
            task["description"] = description
            break
    write_json(json_filepath, tasks_json)
    return


def delete_task(json_filepath, _id):
    tasks_json = read_json(json_filepath)
    for i, task in enumerate(tasks_json["tasks"]):
        if task["id"] == _id:
            tasks_json["tasks"].pop(i)
            break
    write_json(json_filepath, tasks_json)
    return


def mark_task_status(json_filepath, _id, status):
    tasks_json = read_json(json_filepath)
    for i, task in enumerate(tasks_json["tasks"]):
        if task["id"] == _id:
            task["status"] = status
            break
    write_json(json_filepath, tasks_json)
    return


def list_tasks(json_filepath, status):
    tasks_json = read_json(json_filepath)
    tasks_list = tasks_json["tasks"]
    if status:
        tasks_list = [task for task in tasks_list if task["status"] == status]
    return tasks_list


def main():
    # create the json file if doesn't exist
    if not os.path.isfile(JSON_FILEPATH):
        write_json(JSON_FILEPATH, {"metadata": {"num_tasks": 0}, "tasks": []})

    # parse cli args
    parser = argparse.ArgumentParser(
        prog="task-cli", description="To-do list cli application"
    )
    parser.set_defaults(which=None)
    subparsers = parser.add_subparsers()
    # add
    task_adder = subparsers.add_parser("add")
    task_adder.add_argument("description", type=str)
    task_adder.set_defaults(which="add")
    # update
    task_updater = subparsers.add_parser("update")
    task_updater.add_argument("id", type=int)
    task_updater.add_argument("description", type=str)
    task_updater.set_defaults(which="update")
    # delete
    task_deleter = subparsers.add_parser("delete")
    task_deleter.add_argument("id", type=int)
    task_deleter.set_defaults(which="delete")
    # mark-in-progress
    task_mark_in_progress = subparsers.add_parser("mark-in-progress")
    task_mark_in_progress.add_argument("id", type=int)
    task_mark_in_progress.set_defaults(which="mark-in-progress")
    # mark-done
    task_mark_done = subparsers.add_parser("mark-done")
    task_mark_done.add_argument("id", type=int)
    task_mark_done.set_defaults(which="mark-done")
    # list
    task_lister = subparsers.add_parser("list")
    task_lister.add_argument("status", default=None)
    task_lister.set_defaults(which="list")

    args = parser.parse_args()

    match args.which:
        case "add":
            return add_task(JSON_FILEPATH, args.description)
        case "update":
            return update_task(JSON_FILEPATH, args.id, args.description)
        case "delete":
            return delete_task(JSON_FILEPATH, args.id)
        case "mark-in-progress":
            return mark_task_status(JSON_FILEPATH, args.id, "in-progress")
        case "mark-done":
            return mark_task_status(JSON_FILEPATH, args.id, "done")
        case "list":
            return list_tasks(JSON_FILEPATH, args.status)
        case None:
            parser.print_help()
            return
    return


if __name__ == "__main__":
    main()
