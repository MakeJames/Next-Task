"""Test the methods of the tasks module."""

import sqlite3
import pytest
from next_task.services import tasks
from next_task.database import store

from pytest_mock import mocker


class TestCreateTask:
    """Test the Create Task class."""

    @pytest.mark.integration
    def test_create_task(self, mock_database, empty_db, capsys):
        """R-BICEP: Right."""
        expected = "Created Task 1: a test task\n"
        task = tasks.CreateTask("a test task")
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.integration
    def test_sql_injection(self, mock_database, empty_db):
        """R-BICEP: Right."""
        expected = 1
        task = tasks.CreateTask("a test task); DROP TABLE task")
        with store.Connection() as conn:
            conn.curs.execute("SELECT COUNT(*) FROM task;")
            res = conn.curs.fetchone()
        assert res[0] == expected

    def test_creation(self, mock_write, capsys):
        """R-BICEP: Right."""
        expected = "Created Task 1: a test task\n"
        task = tasks.CreateTask("a test task")
        captured = capsys.readouterr()
        assert captured.out == expected

    def test_creation_with_markup(self, mock_write, capsys):
        """R-BICEP: Right."""
        expected = "Created Task 1: a test [info]task[/info]\n"
        task = tasks.CreateTask("a test [info]task[/info]")
        captured = capsys.readouterr()
        assert captured.out == expected


class TestGetNextTask:
    """Test the methods of the get next task class."""

    task_1 = {"task_id": 1, "summary": "a mock task"}
    task_2 = {"task_id": 2, "summary": "Make a cup of Tea"}
    task_430 = {"task_id": 430, "summary": "A mocked test task"}

    @pytest.mark.integration
    def test_when_empty_db_then_task_is_NoneType(self, empty_db):
        """R-BICEP: Right."""
        expected = []
        test = tasks.GetNextTask()
        assert test.task == expected

    @pytest.mark.integration
    def test_get_next_task_when_tasks_in_db(self, test_db):
        """R-BICEP: Right."""
        expected_id = 1
        expected_summary = "A task"
        test = tasks.GetNextTask()
        assert test.task[0][0] == expected_id \
            and test.task[0][1] == expected_summary

    @pytest.mark.parametrize('mock_read', [[]], indirect=['mock_read'])
    def test_when_no_tasks_in_db_then_confirm_is_false(self, mock_read):
        """R-BICEP: Right."""
        expected = False
        test = tasks.GetNextTask()
        assert test.confirm_next_task() == expected

    @pytest.mark.parametrize('mock_read', [[task_1]], indirect=['mock_read'])
    def test_when_tasks_in_db_then_confirm_is_true(self, mock_read):
        """R-BICEP: Right."""
        expected = True
        test = tasks.GetNextTask()
        assert test.confirm_next_task() == expected

    @pytest.mark.parametrize('mock_read', [[task_430]], indirect=['mock_read'])
    def test_when_tasks_in_db_then_print_task(self, mock_read, capsys):
        """R-BICEP: Right."""
        expected = "430: A mocked test task\n"
        test = tasks.GetNextTask()
        test.print()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.parametrize('mock_read', [[]], indirect=['mock_read'])
    def test_when_no_tasks_then_exit_msg(self, mock_read, capsys):
        """R-BICEP: Right."""
        expected = ("Congratulations! There are no more tasks on your "
                    "task list\nTake a break and have a cup of tea.\n")
        test = tasks.GetNextTask()
        test.print()
        captured = capsys.readouterr()
        assert captured.out == expected


class TestSkipTaskClass:
    """Test the Methods of the Skip class."""

    task_1 = {"task_id": 1, "summary": "a mock task"}
    task_2 = {"task_id": 2, "summary": "Make a cup of Tea"}

    @pytest.mark.integration
    def test_when_task_then_skip(self, test_db, capsys):
        """R-BICEP: Right."""
        expected = "Skipped Task 1\n2: Make a cup of tea\n"
        test = tasks.SkipTask()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.integration
    def test_when_no_tasks_then_exit_msg(self, empty_db, capsys):
        """R-BICEP: Right."""
        expected = ("Congratulations! There are no more tasks on your "
                    "task list\nTake a break and have a cup of tea.\n")
        test = tasks.SkipTask()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.integration
    def test_when_only_one_task(self, empty_db, capsys):
        """R-BICEP: Right."""
        expected = ("Created Task 1: A test task\n"
                    "Skipped Task 1\n1: A test task\n")
        tasks.CreateTask("A test task")
        test = tasks.SkipTask()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.parametrize('mock_read', [[task_1, task_2, ]],
                             indirect=['mock_read'])
    def test_when_task_then_skip(self, mock_read, mock_write, capsys):
        """R-BICEP: Right."""
        expected = "Skipped Task 1\n2: Make a cup of Tea\n"
        test = tasks.SkipTask()
        captured = capsys.readouterr()
        assert captured.out == expected


class TestCloseClass:
    """Test the methods of the Close Task class."""

    task_1 = {"task_id": 1, "summary": "a mock task"}
    task_2 = {"task_id": 2, "summary": "Make a cup of Tea"}

    @pytest.mark.parametrize('mock_read', [[task_1, task_2, ]],
                             indirect=['mock_read'])
    def test_when_task_then_close_task(self, mock_read, mock_write, capsys):
        """R-BICEP: Right."""
        expected = "Closed 1: a mock task\n2: Make a cup of Tea\n"
        test = tasks.CloseTask()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.parametrize('mock_read', [[]], indirect=['mock_read'])
    def test_when_no_task_then_exit_msg(self, mock_read, mock_write, capsys):
        """R-BICEP: Right."""
        expected = ("Congratulations! There are no more tasks on your "
                    "task list\nTake a break and have a cup of tea.\n")
        test = tasks.CloseTask()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.integration
    def test_when_task_then_close_task(self, test_db, capsys):
        """R-BICEP: Right."""
        expected = "Closed 1: A task\n2: Make a cup of tea\n"
        test = tasks.CloseTask()
        captured = capsys.readouterr()
        assert captured.out == expected


class TestListClass:
    """Test the methods of the list task class."""

    task_1 = {"task_id": 1, "summary": "a mock task"}
    task_2 = {"task_id": 2, "summary": "Make a cup of Tea"}

    @pytest.mark.parametrize('mock_read', [[]], indirect=['mock_read'])
    def test_when_no_task_then_exit_msg(self, mock_read, capsys):
        """R-BICEP: Right."""
        expected = ("")
        test = tasks.ListTasks()
        captured = capsys.readouterr()
        assert captured.out == expected

    @pytest.mark.integration
    def test_when_tasks_then_list_tasks(self, test_db, capsys):
        """R-BICEP: Right."""
        expected = ("Open Tasks")
        test = tasks.ListTasks()
        captured = capsys.readouterr()
        assert expected in captured.out
