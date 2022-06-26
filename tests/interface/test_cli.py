"""Test the methods of the cli module."""

from pathlib import Path
import pytest
import json

from pytest_mock import mocker

from next_task.interface import cli
from next_task.services import tasks
from next_task import __version__


class TestCliMainMethod:
    """Test the main method of the cli module."""

    def test_main_version(self, capsys) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--version"])
        captured = capsys.readouterr()
        assert captured.out == f"Next: {__version__}"

    def test_task_creation(self, capsys) -> None:
        """R-BICEP: Right."""
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

    def test_that_next_task_is_returned(
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

        cli.main(["--task"])
        captured = capsys.readouterr()
        assert "5102" in captured.out

    @pytest.fixture
    def mock_json_dump(self, mocker):
        """Mock the write aspect of the writer function."""
        mocker.patch("json.dump")

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

    def test_when_skipped_next_task_is_returned(
        self,
        mocker,
        mock_get_next_task,
        mock_json_dump,
        capsys
    ) -> None:
        """R-BICEP: Right."""

        def mock_file_path():
            return "tests/data_mocks/task_file"

        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

        cli.main(["--skip"])
        captured = capsys.readouterr()
        assert "updated 5102" in captured.out

    def test_when_closed_task_is_closed(
        self,
        mock_get_next_task,
        mock_json_dump,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        cli.main(["--done"])
        captured = capsys.readouterr()
        assert "Updated 5102" \
            in captured.out
