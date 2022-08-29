"""Test the methods of the tasks module."""

import pytest
from pathlib import Path
from loguru import logger
from pytest_mock import mocker
import datetime
from time import time

from next_task.services import store
from next_task.services import tasks


class TestCreateTask:
    """Test the methods to creating a task."""

    def test_when_there_are_no_tasks_then_id_is_one(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask(0, "test_call")
        assert test_call.id == 1

    def test_when_summary_is_passed_as_int_then_stored_as_str(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask(4, 4)

        assert test_call.summary == "4"

    def test_when_summary_is_passed_as_bool_then_stored_as_str(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask(4, False)

        assert test_call.summary == "False"


class TestGetNextTask:
    """Test the get Next Task class."""

    def test_when_next_task_is_identified_then_print_task(
        self,
        capsys,
        mock_write,
        test_data_mock
    ) -> None:
        """R-BICEP: Right."""
        tasks.GetNextTask(test_data_mock).print_task()
        captured = capsys.readouterr()
        assert "5102" in captured.out

    def test_when_task_data_is_empty_then_error(
        self,
        capsys,
        mock_write
    ) -> None:
        """R-BICEP: Right."""
        class test:
            current_task = {}
            current_project = {}
            tasks = []
        tasks.GetNextTask(test())
        captured = capsys.readouterr()
        assert "Congratulations!" in captured.out


class TestSkipTask:
    """Test the methods of the Skip task class."""

    def test_when_called_due_date_of_task_is_increased(
        self,
        mock_task_file,
        mock_write
    ) -> None:
        """R-BICEP: Right."""
        class task_data:
            current_task = {"id": 1, "status": "open"}
            current_project = {}
            tasks = [{"id": 1, "status": "open", "skip_count": 0}]

        test_call = tasks.SkipTask(task_data())
        test_call.skip_task["skip_count"] == 1


class TestMarkAsClosedClass:
    """Test the methods of the Mark as closed class."""

    def test_when_called_task_is_closed(
        self,
        mock_task_file,
        mock_write,
    ) -> None:
        """R-BICEP: Right."""
        class task_data:
            current_task = {"id": 1, "status": "open"}
            current_project = {}
            tasks = [{"id": 1, "status": "open"}]
            completed_tasks = []
            pass
        test_call = tasks.MarkAsClosed(task_data())
        closed_task = test_call.closed_task
        completed_tasks = test_call.task_data.completed_tasks
        assert closed_task["status"] == "closed" \
            and completed_tasks[-1]["id"] == closed_task["id"]


class TestTimeStamp:
    """Test the methods of the TimeStampClass."""

    def test_TimeStamp_now_is_correctly_formatted(self):
        """R-BICEP: Right."""
        t = tasks.TimeStamp().now
        assert datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

    def test_TimeStamp_convert_from_string_returns_datetime_object(self):
        """R-BICEP: Right."""
        t = datetime.datetime.now()
        t_string = t.strftime("%Y-%m-%d %H:%M:%S")
        t_date_time = datetime.datetime.strptime(t_string, "%Y-%m-%d %H:%M:%S")
        test = tasks.TimeStamp().convert_from_string(t_string)
        assert test == t_date_time \
            and isinstance(test, datetime.datetime)

    def test_convert_from_string_returns_datetime_when_passed_datetime(self):
        """R-BICEP: Boundary."""
        t = datetime.datetime.now()
        test = tasks.TimeStamp().convert_from_string(t)
        assert t == test

    def test_TimeStamp_convert_to_string_returns_string(self):
        """R-BICEP: Right."""
        t = datetime.datetime.now()
        test = tasks.TimeStamp().convert_to_string(t)
        assert t.strftime("%Y-%m-%d %H:%M:%S") == test \
            and isinstance(test, str)

    def test_convert_to_string_returns_string_when_passed_string(self):
        """R-BICEP: Boundary."""
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test = tasks.TimeStamp().convert_to_string(t)
        assert t == test

    def test_TimeStamp_short_returns_short_date_(self):
        """R-BICEP: Right."""
        t = tasks.TimeStamp().now
        t_short = tasks.TimeStamp().short(t)
        assert datetime.datetime.strptime(t_short, "%Y-%m-%d")
