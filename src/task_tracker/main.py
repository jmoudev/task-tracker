import argparse
import os
import pprint

import task_tracker.tasks as tasks


JSON_FILENAME = "tasks.json"
JSON_FILEPATH = os.path.join(os.curdir, JSON_FILENAME)


def main(json_filepath=JSON_FILEPATH):
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
    task_lister.add_argument(
        "status", nargs="?", type=str, choices=["todo", "in-progress", "done"]
    )
    task_lister.set_defaults(which="list")

    args = parser.parse_args()

    match args.which:
        case "add":
            pprint.pprint(tasks.TasksFile(json_filepath).add_task(args.description))
        case "update":
            pprint.pprint(
                tasks.TasksFile(json_filepath).update_task_description(
                    args.id, args.description
                )
            )
        case "delete":
            pprint.pprint(tasks.TasksFile(json_filepath).delete_task(args.id))
        case "mark-in-progress":
            pprint.pprint(
                tasks.TasksFile(json_filepath).update_task_status(
                    args.id, "in-progress"
                )
            )
        case "mark-done":
            pprint.pprint(
                tasks.TasksFile(json_filepath).update_task_status(args.id, "done")
            )
        case "list":
            pprint.pprint(
                tasks.TasksFile(json_filepath).list_tasks_by_status(args.status)
            )
        case None:
            parser.print_help()


if __name__ == "__main__":
    main()
