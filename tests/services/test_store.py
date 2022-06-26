"""Test the methods of the file module."""

import pytest
import json
from loguru import logger
from pathlib import Path
from pytest_mock import mocker

from next_task.services import store


class TestCheckTaskStoreClass:
    """Test the methods of the Check class."""

    def test_when_task_file_does_not_exit_then_file_is_created(self) -> None:
        """R-BICEP: Right."""
        assert Path(f"{str(Path.home())}/.tasks.json").exists() is False
        assert store.CheckTaskStore()
        assert Path(f"{str(Path.home())}/.tasks.json").exists() is True

    def test_when_file_exists_then_existing_data_is_not_overwritten(
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
        captured = capsys.readouterr()
        store.CheckTaskStore()
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            file_data = json.load(file)
        assert len(file_data["tasks"]) == 2


class TestWriteTask:
    """Test the methods of the Write Task class."""

    @pytest.fixture(autouse=True)
    def mock_json_dump(self, mocker):
        """Ensure that data is not added to test file."""
        mocker.patch("json.dump")

    def test_when_dictionary_is_empty_then_data_corrected(self) -> None:
        """R-BICEP: Error."""
        assert "tasks" in store.WriteTask(data={}).data

    def test_when_task_list_is_empty_then_file_format_corrected(self) -> None:
        """R-BICEP: Error."""
        assert "completed" in store.WriteTask(data={"tasks": []}).data

    def test_when_wrong_type_is_supplied_then_format_corrected(self) -> None:
        """R-BICEP: Error."""
        assert "tasks" in store.WriteTask(True).data


class TestCheckTasks:
    """Test the Methods of the Check Tasks class."""

    def test_when_data_is_empty_dict_then_data_is_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {}
        assert "tasks" in store.CheckTasks(data).data

    def test_when_tasks_is_not_in_dict_then_data_is_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {"tests": 400}
        assert "tasks" in store.CheckTasks(data).data

    def test_when_tasks_data_is_not_a_list_then_data_reformated(self) -> None:
        """R-BICEP: Right."""
        data = {"tasks": 1}
        assert type(store.CheckTasks(data).data["tasks"]) == list

    def test_when_data_is_an_empty_string_then_dict_reformatted(self) -> None:
        """R-BICEP: Right."""
        data = ""
        assert type(store.CheckTasks(data).data) == dict

    def test_when_data_is_present_then_data_is_not_overwritten(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks_1.json", "r") as file:
            file_data = json.load(file)
        assert len(store.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])

    def test_when_data_is_present_then_data_is_not_overwritten(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            file_data = json.load(file)
        assert len(store.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])

    def test_when_tasks_are_empty_then_data_is_retained(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            file_data = json.load(file)
        assert len(store.CheckTasks(file_data).data["completed"]["tasks"]) \
            == len(file_data["completed"]["tasks"])

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/pre_0.3.0/.tasks.json", "r") as file:
            file_data = json.load(file)
        assert len(store.CheckTasks(file_data).data["tasks"]) \
            == len(file_data["tasks"])


class TestCheckTaskCount:
    """Test the check task count class."""

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/pre_0.3.0/.tasks.json", "r") as file:
            file_data = json.load(file)
        test = store.CheckCompleted(file_data).data
        assert store.CheckTaskCount(test).data["task_count"] == 4


class TestCheckCompleted:
    """Test the check migration of completed issues to a completed list."""

    def test_when_checked_pre_0_3_0_files_are_compatable(self) -> None:
        """R-BICEP: Right."""
        with open("tests/data_mocks/pre_0.3.0/.tasks.json", "r") as file:
            file_data = json.load(file)
        test = store.CheckCompleted(file_data).data
        assert len(test["completed"]["tasks"]) == 2
