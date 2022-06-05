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
        assert len(file_data["tasks"]) == 4
