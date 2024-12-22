import datetime
import json


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
