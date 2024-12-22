import os
import tempfile
import unittest

import task_tracker.utils as utils
import task_tracker.tasks as tasks


class TestTaskOperation(unittest.TestCase):
    tasks_json_filename = "tasks.json"

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.tasks_json_filename
        )
        utils.create_tasks_json(self.tasks_json_filepath)
        self.tasks_file = tasks.TasksFile(self.tasks_json_filepath)

    def tearDown(self):
        self.tempdir.cleanup()


class TestTaskAdd(TestTaskOperation):
    def test_task_add(self):
        # add 1
        self.tasks_file.add_task("A task")
        task_add_file_1 = utils.read_json(self.tasks_json_filepath)
        task_add_tasks_1 = task_add_file_1["tasks"]
        self.assertEqual(task_add_file_1["metadata"]["task_counter"], 1)
        self.assertEqual(len(task_add_tasks_1), 1)
        self.assertEqual(task_add_tasks_1["1"]["id"], 1)
        self.assertEqual(task_add_tasks_1["1"]["description"], "A task")
        self.assertEqual(task_add_tasks_1["1"]["status"], "todo")
        # add 2
        self.tasks_file.add_task("Another task")
        task_add_2_file = utils.read_json(self.tasks_json_filepath)
        task_add_2_tasks = task_add_2_file["tasks"]
        self.assertEqual(task_add_2_file["metadata"]["task_counter"], 2)
        self.assertEqual(len(task_add_2_tasks), 2)
        self.assertEqual(task_add_2_tasks["2"]["id"], 2)
        self.assertEqual(task_add_2_tasks["2"]["description"], "Another task")


class TestWithPredefinedTasks(TestTaskOperation):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.tasks_json_filename
        )
        utils.write_json(
            self.tasks_json_filepath,
            {
                "tasks": {
                    "1": {
                        "id": 1,
                        "description": "A task",
                        "status": "todo",
                        "createdAt": utils.get_iso_datetime(),
                        "updatedAt": utils.get_iso_datetime(),
                    },
                    "2": {
                        "id": 2,
                        "description": "Another task",
                        "status": "todo",
                        "createdAt": utils.get_iso_datetime(),
                        "updatedAt": utils.get_iso_datetime(),
                    },
                }
            },
        )
        self.tasks_file = tasks.TasksFile(self.tasks_json_filepath)


class TestTaskUpdate(TestWithPredefinedTasks):
    def test_task_update(self):
        # pre update
        task_update_file_0 = utils.read_json(self.tasks_json_filepath)
        self.tasks_file.update_task_description(1, "An updated task")
        # update 1
        task_update_file_1 = utils.read_json(self.tasks_json_filepath)
        self.assertEqual(task_update_file_1["tasks"]["1"]["id"], 1)
        self.assertEqual(
            task_update_file_1["tasks"]["1"]["description"], "An updated task"
        )
        self.assertGreater(
            task_update_file_1["tasks"]["1"]["updatedAt"],
            task_update_file_0["tasks"]["1"]["updatedAt"],
        )


class TestTaskDelete(TestWithPredefinedTasks):
    def test_task_delete(self):
        # delete 1
        task_delete_output_1 = self.tasks_file.delete_task(1)
        task_delete_tasks_1 = utils.read_json(self.tasks_json_filepath)["tasks"]
        self.assertEqual(task_delete_output_1, "Task deleted successfully (ID: 1)")
        self.assertEqual(len(task_delete_tasks_1), 1)
        # delete 2
        task_delete_output_2 = self.tasks_file.delete_task(2)
        task_delete_tasks_2 = utils.read_json(self.tasks_json_filepath)["tasks"]
        self.assertEqual(task_delete_output_2, "Task deleted successfully (ID: 2)")
        self.assertEqual(len(task_delete_tasks_2), 0)

    def test_task_delete_unsuccessful(self):
        # delete 1
        self.tasks_file.delete_task(1)
        # delete 1 expecting failure
        with self.assertRaises(tasks.TaskKeyError):
            self.tasks_file.delete_task(1)


class TestTasksMarkStatus(TestWithPredefinedTasks):
    def test_task_mark_in_progress(self):
        # pre mark in-progress
        task_mark_in_progress_task_0 = utils.read_json(self.tasks_json_filepath)[
            "tasks"
        ]["1"]
        self.assertEqual(task_mark_in_progress_task_0["status"], "todo")
        # mark in-progress 1
        self.tasks_file.update_task_status(1, "in-progress")
        task_mark_in_progress_task_1 = utils.read_json(self.tasks_json_filepath)[
            "tasks"
        ]["1"]
        self.assertEqual(task_mark_in_progress_task_1["status"], "in-progress")
        self.assertGreater(
            task_mark_in_progress_task_1["updatedAt"],
            task_mark_in_progress_task_0["updatedAt"],
        )

    def test_task_mark_done(self):
        # pre mark done
        task_mark_done_task_0 = utils.read_json(self.tasks_json_filepath)["tasks"]["1"]
        self.assertEqual(task_mark_done_task_0["status"], "todo")
        # mark done 1
        self.tasks_file.update_task_status(1, "done")
        task_mark_done_task_1 = utils.read_json(self.tasks_json_filepath)["tasks"]["1"]
        self.assertEqual(task_mark_done_task_1["status"], "done")
        self.assertGreater(
            task_mark_done_task_1["updatedAt"], task_mark_done_task_0["updatedAt"]
        )


class TestWithPredefinedMarkedTasks(TestTaskOperation):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.tasks_json_filepath = os.path.join(
            self.tempdir.name, self.tasks_json_filename
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
        self.tasks_file = tasks.TasksFile(self.tasks_json_filepath)


class TestTasksList(TestWithPredefinedMarkedTasks):
    def test_tasks_list(self):
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
        # list all 1
        tasks_list_output = self.tasks_file.list_tasks_by_status(None)
        self.assertListEqual(tasks_list_output, expected_tasks_list)

    def test_tasks_list_by_status(self):
        expected_tasks_list = [
            {
                "id": 2,
                "description": "Another task",
                "status": "done",
            }
        ]
        # list done 1
        tasks_list_done_output = self.tasks_file.list_tasks_by_status("done")
        self.assertListEqual(tasks_list_done_output, expected_tasks_list)


if __name__ == "__main__":
    unittest.main()
