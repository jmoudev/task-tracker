import os
import tempfile
import unittest

import task_tracker.utils as utils
import task_tracker.tasks as tasks


class TestTaskOperation(unittest.TestCase):
    TASKS_JSON_FILENAME = "tasks.json"

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.TASKS_JSON_FILENAME
        )
        utils.create_tasks_json(self.tasks_json_filepath)
        return

    def tearDown(self):
        self.tempdir.cleanup()
        return


class TestTaskAdd(TestTaskOperation):
    def test_task_add(self):
        # test add task 1
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        tasks_file.add_task("A task")
        tasks_json = utils.read_json(self.tasks_json_filepath)
        self.assertEqual(tasks_json["metadata"]["task_counter"], 1)
        self.assertEqual(len(tasks_json["tasks"]), 1)
        self.assertEqual(tasks_json["tasks"]["1"]["id"], 1)
        self.assertEqual(tasks_json["tasks"]["1"]["description"], "A task")
        self.assertEqual(tasks_json["tasks"]["1"]["status"], "todo")
        # test add task 2
        tasks_file.add_task("Another task")
        tasks_json = utils.read_json(self.tasks_json_filepath)
        self.assertEqual(tasks_json["metadata"]["task_counter"], 2)
        self.assertEqual(len(tasks_json["tasks"]), 2)
        self.assertEqual(tasks_json["tasks"]["2"]["id"], 2)
        self.assertEqual(tasks_json["tasks"]["2"]["description"], "Another task")
        return


class TestWithPredefinedTasks(TestTaskOperation):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.TASKS_JSON_FILENAME
        )
        utils.write_json(
            self.tasks_json_filepath,
            {
                "tasks": {
                    "1": {
                        "id": 1,
                        "description": "A task",
                        "status": "todo",
                        "updatedAt": utils.get_iso_datetime(),
                    },
                    "2": {
                        "id": 2,
                        "description": "Another task",
                        "status": "todo",
                        "updatedAt": utils.get_iso_datetime(),
                    },
                }
            },
        )
        return


class TestTaskUpdate(TestWithPredefinedTasks):
    def test_task_update(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        # test update task
        tasks_json_pre_update = utils.read_json(self.tasks_json_filepath)
        tasks_file.update_task_description(1, "An updated task")
        tasks_json = utils.read_json(self.tasks_json_filepath)
        self.assertEqual(tasks_json["tasks"]["1"]["id"], 1)
        self.assertEqual(tasks_json["tasks"]["1"]["description"], "An updated task")
        self.assertGreater(
            tasks_json["tasks"]["1"]["updatedAt"],
            tasks_json_pre_update["tasks"]["1"]["updatedAt"],
        )
        return


class TestTaskDelete(TestWithPredefinedTasks):
    def test_task_delete(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        # test delete task
        tasks_json_pre_delete = utils.read_json(self.tasks_json_filepath)
        tasks_file.delete_task(1)
        tasks_json = utils.read_json(self.tasks_json_filepath)
        self.assertEqual(len(tasks_json_pre_delete["tasks"]), 2)
        self.assertEqual(len(tasks_json["tasks"]), 1)
        tasks_file.delete_task(2)
        return


class TestTasksMarkStatus(TestWithPredefinedTasks):
    def test_task_mark_in_progress(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        task_without_marked_status = utils.read_json(self.tasks_json_filepath)["tasks"][
            "1"
        ]
        tasks_file.update_task_status(1, "in-progress")
        task_marked_in_progress = utils.read_json(self.tasks_json_filepath)["tasks"][
            "1"
        ]
        self.assertEqual(task_without_marked_status["status"], "todo")
        self.assertEqual(task_marked_in_progress["status"], "in-progress")
        self.assertGreater(
            task_marked_in_progress["updatedAt"],
            task_without_marked_status["updatedAt"],
        )
        return

    def test_task_mark_done(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        task_without_marked_status = utils.read_json(self.tasks_json_filepath)["tasks"][
            "1"
        ]
        tasks_file.update_task_status(1, "done")
        task_marked_done = utils.read_json(self.tasks_json_filepath)["tasks"]["1"]
        self.assertEqual(task_without_marked_status["status"], "todo")
        self.assertEqual(task_marked_done["status"], "done")
        self.assertGreater(
            task_marked_done["updatedAt"], task_without_marked_status["updatedAt"]
        )
        return


class TestWithPredefinedMarkedTasks(TestTaskOperation):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.TASKS_JSON_FILENAME
        )
        utils.write_json(
            self.tasks_json_filepath,
            {
                "tasks": {
                    "1": {
                        "id": 1,
                        "description": "A task",
                        "status": "in-progress",
                    },
                    "2": {
                        "id": 2,
                        "description": "Another task",
                        "status": "done",
                    },
                }
            },
        )
        return


class TestTasksList(TestWithPredefinedMarkedTasks):
    def test_tasks_list(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        expected_tasks_list = [
            {
                "id": 1,
                "description": "A task",
                "status": "in-progress",
            },
            {
                "id": 2,
                "description": "Another task",
                "status": "done",
            },
        ]
        tasks_list = tasks_file.list_tasks_by_status(None)
        self.assertListEqual(tasks_list, expected_tasks_list)
        return

    def test_tasks_list_by_status(self):
        tasks_file = tasks.TasksFile(self.tasks_json_filepath)
        expected_tasks_list = [
            {
                "id": 2,
                "description": "Another task",
                "status": "done",
            }
        ]
        tasks_list = tasks_file.list_tasks_by_status("done")
        self.assertListEqual(tasks_list, expected_tasks_list)
        return


if __name__ == "__main__":
    unittest.main()
