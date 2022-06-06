"""Test the methods of the file module."""

import pytest
import json
from loguru import logger
from pathlib import Path
from pytest_mock import mocker

from next_task.services import store


class TestCheckClass:
    """Test the methods of the Check class."""

    def test_when_task_file_does_not_exit_then_file_is_created(self) -> None:
        """R-BICEP: Right."""
        _file = store.Check()
        with open(_file.file, "r") as file:
            _file_data = json.load(file)
        assert Path(_file.file).exists() \
            and "tasks" in _file_data

    def test_when_file_exists_then_existing_data_is_not_overwritten(
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
        captured = capsys.readouterr()
        with open("tests/data_mocks/tasks_1.json", "r") as file:
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
        assert "completed_tasks" in store.WriteTask(data={"tasks": []}).data

    def test_when_wrong_type_is_supplied_then_error(self) -> None:
        """R-BICEP: Error."""
        assert "tasks" in store.WriteTask(True).data
