"""Test the methods of the tasks module."""

import pytest
import json
from loguru import logger
from pytest_mock import mocker
import datetime
from time import time

from next_task.services import store
from next_task.services import tasks


class TestCreateTask:
    """Test the methods to creating a task."""

    @pytest.fixture
    def mock_tasks_file(self, mocker) -> None:
        """Return a file in the mock data file."""
        def mock_file_path():
            return "tests/data_mocks/tasks_2.json"
        mocker.patch.object(
            store.Check,
            "_file_path_builder",
            return_value=mock_file_path()
        )

    def test_when_there_are_no_tasks_then_id_is_one(self):
        """R-BICEP: Right."""
        test_call = tasks.CreateTask("test_call")
        with open(store.Check().file, "r") as file:
            file_data = json.load(file)
            print(json.dumps(file_data, indent=4))

        assert test_call.id == 1 \
            and file_data["tasks"][0]["id"] == 1

    def test_when_there_are_a_thousand_tasks_then_creation_is_performative(
        self,
        mock_tasks_file,
        mocker
    ) -> None:
        """R-BICEP: Performance."""
        mocker.patch("json.dump")
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

    def test_when_next_task_is_identified_then_print_task(
        self,
        capsys,
        mocker
    ) -> None:
        """R-BICEP: Right."""
        def mock_file_path():
            return "tests/data_mocks/tasks_1.json"
        mocker.patch.object(
            store.Check,
            "_file_path_builder",
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

    @pytest.fixture
    def mock_json_dump(self, mocker):
        """Mock the write aspect of the writer function."""
        mocker.patch("json.dump")

    @pytest.fixture
    def mock_get_next_task(self, mocker):
        """Mock the catalogue check, file_path builder method."""

        def mock_file():
            return "tests/data_mocks/tasks_1.json"

        mocker.patch.object(
            store.Check,
            "_file_path_builder",
            return_value=mock_file()
        )

    def test_when_called_task_is_skipped(
        self,
        mock_get_next_task,
        mock_json_dump
    ) -> None:
        """R-BICEP: Right."""
        test_call = tasks.SkipTask()
        due_1 = datetime.datetime.strptime(
            "2022-06-12 09:00:28",
            "%Y-%m-%d %H:%M:%S"
        )
        due_2 = datetime.datetime.strptime(
            test_call.task["due"],
            "%Y-%m-%d %H:%M:%S"
        )
        assert due_1 < due_2
