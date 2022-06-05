"""Test the methods of the tasks module."""

from enum import auto
import pytest
import json
from loguru import logger
from pytest_mock import mocker
import datetime
from time import time

from next_task.services import store
from next_task.services import tasks


class TestFetchLastIdClass:
    """Validate the methods of the Fetch last id class."""

    def test_when_there_are_no_tasks_then_task_index_is_zero(self) -> None:
        """R-BICEP: Right."""
        data = {"tasks": []}
        id = tasks.FetchLastId(data).id
        assert id == 0

    def test_when_there_are_two_tasks_then_task_index_is_two(self) -> None:
        """R-BICEP: Right."""
        data = {
            "tasks": [
                {"id": 1},
                {"id": 2}
            ]
        }
        id = tasks.FetchLastId(data).id
        assert id == 2

    def test_when_data_is_an_empty_string_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(KeyError):
            # This is currently erroring on tasks not being in the data
            data = ""
            tasks.FetchLastId(data)

    def test_when_data_is_a_string_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(TypeError):
            # currently relies on a the string indicies of the dictionary
            data = "tasks"
            tasks.FetchLastId(data)

    def test_when_data_is_an_integer_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(TypeError):
            # currently caught when trying to itterate through a string
            data = 1000
            tasks.FetchLastId(data)

    def test_when_data_is_empty_dictionary_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(NameError):
            data = {}
            tasks.FetchLastId(data)

    def test_when_tasks_data_is_not_a_list_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(AttributeError):
            data = {"tasks": 1}
            tasks.FetchLastId(data)

    def test_when_tasks_is_not_in_data_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(KeyError):
            data = {
                "projects": [
                    {"name": "home"}
                ],
                "name": "test_data"
            }
            tasks.FetchLastId(data)


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


class TestFilterOpenTasks:
    """Test the methods of the filter open tasks."""

    def test_that_closed_tasks_are_removed_from_working_dictionary(
        self
    ) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_1.json", "r") as file:
            file_data = json.load(file)
        test_data = tasks.FilterOpenTasks(file_data).data
        logger.debug(test_data)
        assert len(test_data) == 2
        assert test_data[0]["id"] == 5101

    def test_that_closed_tasks_are_removed_performatvely(
        self
    ) -> None:
        """R-BICEP: Performance."""
        with open("tests/data_mocks/tasks_2.json", "r") as file:
            file_data = json.load(file)
        start = time()
        tasks.FilterOpenTasks(file_data).data
        end = time()
        dif = (end - start)
        assert dif < 0.1


class TestGetPriority:
    """Test the methods of the priority calculation class."""

    def test_when_called_higest_priority_task_is_returned(
        self
    ) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_1.json", "r") as file:
            file_data = json.load(file)
        test_data = tasks.FilterOpenTasks(file_data).data
        test_call = tasks.GetPriority(test_data)
        assert test_call.data[0]["id"] == 5102

    def test_when_called_higest_priority_task_is_returned_performatvely(
        self
    ) -> None:
        """R-BICEP: Performance."""
        with open("tests/data_mocks/tasks_2.json", "r") as file:
            file_data = json.load(file)
        test_data = tasks.FilterOpenTasks(file_data).data
        start = time()
        tasks.GetPriority(test_data)
        end = time()
        dif = end - start
        logger.debug(dif)
        assert dif <= 1


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


class TestUpdateDueDate:
    """Test the Methods of the Update Due date class."""

    def test_when_provided_data_then_due_date_incrememented_by_one_day(
        self
    ) -> None:
        """R-BICEP: Right."""
        data = {"due": "2022-06-04 20:21:34"}
        test = tasks.UpdateDueDate(data).task
        assert test["due"] == "2022-06-05 20:21:34"

    def test_when_no_data_provided_then_error(self) -> None:
        """R-BICEP: Error."""
        data = {}
        with pytest.raises(KeyError):
            tasks.UpdateDueDate(data)

    def test_when_time_formatting_is_wrong_then_error(self) -> None:
        """R-BICEP: Error."""
        data = {"due": "04-06-2022 20:21"}
        with pytest.raises(ValueError):
            tasks.UpdateDueDate(data)


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
