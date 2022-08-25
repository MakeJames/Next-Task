"""Test the methods of the cli module."""

from pathlib import Path
from random import SystemRandom
import pytest
import json

from pytest_mock import mocker

from next_task.interface import cli
from next_task.services import tasks
from next_task.services import store
from next_task import __version__


class TestCliMainMethod:
    """Test the main method of the cli module."""

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

    def test_main_version(self, capsys) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--version"])
        captured = capsys.readouterr()
        assert captured.out == f"Next: {__version__}"

    def test_task_creation(self, capsys, mock_pathlib_home) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--add", "This is a task"])
        captured = capsys.readouterr()
        assert "Created task 1: This is a task" in captured.out

    def test_task_creation_with_multiple_strings_then_error(
        self,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--add", "This is a task", "This is another task"])
        captured = capsys.readouterr()
        assert "error: unrecognized arguments" in captured.err

    def test_when_add_and_close_are_called_togehter_error_is_returned(
        self,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--add", "This is a task", "--done"])
        captured = capsys.readouterr()
        assert "Invalid argument combination\n" \
            == captured.out

    def test_that_next_task_is_returned(
        self,
        capsys,
        mock_get_next_task,
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--task"])
        captured = capsys.readouterr()
        assert "5102" in captured.out

    def test_when_skipped_next_task_is_returned(
        self,
        mock_get_next_task,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--skip"])
        captured = capsys.readouterr()
        print(captured.out)
        assert "updated 5102" in captured.out

    def test_when_closed_task_is_closed(
        self,
        mock_get_next_task,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--done"])
        captured = capsys.readouterr()
        assert "Updated 5102" \
            in captured.out
