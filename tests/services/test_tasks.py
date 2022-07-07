"""Test the methods of the tasks module."""

import pytest
import json
from pathlib import Path
from loguru import logger
from pytest_mock import mocker
import datetime
from time import time

from next_task.services import store
from next_task.services import tasks


class TestGetPriority:
    """Test the methods of the priority calculation class."""

    def test_when_called_higest_priority_task_is_returned(
        self,
        mocker
    ) -> None:
        """R-BICEP: Right."""
        def mock_file_path():
            return "tests/data_mocks/task_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )
        test_call = store.GetTasks()
        test = tasks.GetPriority(test_call.file_data)
        assert test.data["tasks"][0]["id"] == 5102

    def test_when_called_higest_priority_task_is_returned_performatvely(
        self,
        mocker
    ) -> None:
        """R-BICEP: Performance."""
        def mock_file_path():
            return "tests/data_mocks/large_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )
        test_call = store.GetTasks()

        start = time()
        tasks.GetPriority(test_call.file_data)
        end = time()
        dif = end - start
        print(f"dif greater than 1 second: {dif}")
        assert dif <= 1


class TestCreateTask:
    """Test the methods to creating a task."""

    @pytest.fixture
    def mock_write(self, mocker):
        """Mock the write aspect of the writer function."""
        def mock_function():
            return None
        mocker.patch.object(
            store.WriteTask,
            "__init__",
            return_value=mock_function()
        )

    @pytest.fixture
    def mock_tasks_file(self, mocker) -> None:
        """Return a file in the mock data file."""
        def mock_file_path():
            return "tests/data_mocks/large_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_when_there_are_no_tasks_then_id_is_one(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask("test_call")
        with open(store.CheckTaskStore().file, "r") as file:
            file_data = json.load(file)

        assert file_data["tasks"][0]["id"] == 1

    def test_when_summary_is_passed_as_int_then_stored_as_str(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask(4)
        with open(store.CheckTaskStore().file, "r") as file:
            file_data = json.load(file)

        assert file_data["tasks"][0]["summary"] == "4"

    def test_when_summary_is_passed_as_bool_then_stored_as_str(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask(False)
        with open(store.CheckTaskStore().file, "r") as file:
            file_data = json.load(file)

        assert file_data["tasks"][0]["summary"] == "False"

    def test_when_there_are_a_thousand_tasks_then_creation_is_performative(
        self,
        mock_tasks_file,
        mock_write,
        mocker
    ) -> None:
        """R-BICEP: Performance."""
        start = time()
        tasks.CreateTask(
            "test_when_there_are_a_thousand_tasks " +
            f"{start}"
        )
        end = time()
        dif = (end - start)
        assert dif < 1


class TestGetNextTask:
    """Test the get Next Task class."""

    @pytest.fixture(autouse=True)
    def mock_write(self, mocker):
        """Mock the write aspect of the writer function."""
        def mock_function():
            return None
        mocker.patch.object(
            store.WriteTask,
            "__init__",
            return_value=mock_function()
        )

    def test_when_next_task_is_identified_then_print_task(
        self,
        capsys,
        mocker
    ) -> None:
        """R-BICEP: Right."""
        def mock_file_path():
            return "tests/data_mocks/task_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )
        tasks.GetNextTask().print_task()
        captured = capsys.readouterr()
        assert "5102" in captured.out

    def test_when_task_data_is_empty_then_error(
        self,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            tasks.GetNextTask()
        captured = capsys.readouterr()
        assert "Congratulations!" in captured.out


class TestSkipTask:
    """Test the methods of the Skip task class."""

    @pytest.fixture(autouse=True)
    def mock_write(self, mocker):
        """Mock the write aspect of the writer function."""
        def mock_function():
            return None
        mocker.patch.object(
            store.WriteTask,
            "__init__",
            return_value=mock_function()
        )

    @pytest.fixture
    def mock_get_next_task(self, mocker):
        """Mock the catalogue check, file_path builder method."""

        def mock_file_path():
            return "tests/data_mocks/task_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_when_called_task_is_skipped(
        self,
        mock_get_next_task
    ) -> None:
        """R-BICEP: Right."""
        test_call = tasks.SkipTask()
        due_1 = datetime.datetime.strptime(
            "2022-06-12 09:00:28",
            "%Y-%m-%d %H:%M:%S"
        )
        due_2 = datetime.datetime.strptime(
            test_call.tasks.next_task["due"],
            "%Y-%m-%d %H:%M:%S"
        )
        assert due_1 < due_2


class TestMarkAsClosedClass:
    """Test the methods of the Mark as closed class."""

    @pytest.fixture(autouse=True)
    def mock_write(self, mocker):
        """Mock the write aspect of the writer function."""
        def mock_function():
            return None
        mocker.patch.object(
            store.WriteTask,
            "__init__",
            return_value=mock_function()
        )

    @pytest.fixture
    def mock_get_next_task(self, mocker):
        """Mock the catalogue check, file_path builder method."""

        def mock_file_path():
            return "tests/data_mocks/task_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_when_called_task_is_closed(
        self,
        mock_get_next_task
    ) -> None:
        """R-BICEP: Right."""
        test_call = tasks.MarkAsClosed()
        assert test_call.tasks.next_task["status"] == "closed" \
            and test_call.tasks.file.data["completed"]["tasks"][-1]["id"] == \
            test_call.tasks.next_task["id"]
