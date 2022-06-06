"""Test the methods of the tasks module."""

import pytest
import json
from loguru import logger
from pytest_mock import mocker
import datetime
from time import time

from next_task.services import store
from next_task.services import models


class TestFetchLastIdClass:
    """Validate the methods of the Fetch last id class."""

    def test_when_there_are_no_tasks_then_task_index_is_zero(self) -> None:
        """R-BICEP: Right."""
        data = {"tasks": []}
        id = models.FetchLastId(data).id
        assert id == 0

    def test_when_there_are_two_tasks_then_task_index_is_two(self) -> None:
        """R-BICEP: Right."""
        data = {
            "tasks": [
                {"id": 1},
                {"id": 2}
            ]
        }
        id = models.FetchLastId(data).id
        assert id == 2

    def test_when_data_is_a_string_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(TypeError):
            # currently relies on a the string indicies of the dictionary
            data = "tasks"
            models.FetchLastId(data)

    def test_when_data_is_an_integer_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(TypeError):
            # currently caught when trying to itterate through a string
            data = 1000
            models.FetchLastId(data)

    def test_when_tasks_is_not_in_data_then_error(self) -> None:
        """R-BICEP: Error."""
        with pytest.raises(KeyError):
            data = {
                "projects": [
                    {"name": "home"}
                ],
                "name": "test_data"
            }
            models.FetchLastId(data)


class TestFilterOpenTasks:
    """Test the methods of the filter open tasks."""

    def test_that_closed_tasks_are_removed_from_working_dictionary(
        self
    ) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_1.json", "r") as file:
            file_data = json.load(file)
        test_data = models.FilterOpenTasks(file_data).data
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
        models.FilterOpenTasks(file_data).data
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
        test_data = models.FilterOpenTasks(file_data).data
        test_call = models.GetPriority(test_data)
        assert test_call.data[0]["id"] == 5102

    def test_when_called_higest_priority_task_is_returned_performatvely(
        self
    ) -> None:
        """R-BICEP: Performance."""
        with open("tests/data_mocks/tasks_2.json", "r") as file:
            file_data = json.load(file)
        test_data = models.FilterOpenTasks(file_data).data
        start = time()
        models.GetPriority(test_data)
        end = time()
        dif = end - start
        logger.debug(dif)
        assert dif <= 1


class TestCheckTasks:
    """Test the Methods of the Check Tasks class."""

    def test_when_data_is_empty_dict_then_data_is_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {}
        assert "tasks" in models.CheckTasks(data).data

    def test_when_tasks_is_not_in_dict_then_data_is_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {"tests": 400}
        assert "tasks" in models.CheckTasks(data).data

    def test_when_tasks_data_is_not_a_list_then_data_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {"tasks": 1}
        assert type(models.CheckTasks(data).data["tasks"]) == list

    def test_when_data_is_an_empty_string_then_dict_reformatted(self) -> None:
        """R-BICEP: Right."""
        data = ""
        assert type(models.CheckTasks(data).data) == dict

    def test_when_data_is_present_then_data_is_not_overwritten(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_1.json", "r") as file:
            file_data = json.load(file)
        assert len(models.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])

    def test_when_data_is_present_then_data_is_not_overwritten(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_1.json", "r") as file:
            file_data = json.load(file)
        assert len(models.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])

    def test_when_tasks_are_empty_then_data_is_retained(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/tasks_3.json", "r") as file:
            file_data = json.load(file)
        assert len(models.CheckTasks(file_data).data["completed_tasks"]) \
            == len(file_data["completed_tasks"])

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/0-3-0-tasks.json", "r") as file:
            file_data = json.load(file)
        assert len(models.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])


class TestCheckTaskCount:
    """Test the check task count class."""

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/0-3-0-tasks.json", "r") as file:
            file_data = json.load(file)
        assert models.CheckTaskCount(file_data).data["task_count"] == 5102


class TestCheckCompleted:
    """Test the check migration of completed issues to a completed list."""

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/0-3-0-tasks.json", "r") as file:
            file_data = json.load(file)
        test = models.CheckCompleted(file_data).data
        assert len(test["completed_tasks"]) == 2


class TestCheckCompleted:
    """Test the check migration of completed issues to a completed list."""

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/0-3-0-tasks.json", "r") as file:
            file_data = json.load(file)
        test = models.CheckFormatting(file_data).data
        assert len(test["completed_tasks"]) == 2
