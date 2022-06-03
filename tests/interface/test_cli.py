"""Test the methods of the cli module."""

import pytest

from pytest_mock import mocker

from next_task.services import catalogue
from next_task.interface import cli
from next_task import __version__


class TestCliMainMethod:
    """Test the main method of the cli module."""

    def test_main_version(self, capsys) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--version"])
        captured = capsys.readouterr()
        assert captured.out == f"Next: {__version__}"

    def test_file_checker(self, capsys) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--check-file"])
        captured = capsys.readouterr()
        assert captured.out == "created .tasks.json\n"

    def test_task_creation(self, capsys) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--add", "This is a task"])
        captured = capsys.readouterr()
        assert "Created task 1: This is a task" in captured.out
