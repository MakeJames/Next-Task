"""Test the methods of the cli module."""

from pathlib import Path
import pytest

from pytest_mock import mocker

from next_task import __version__


class TestCliMainMethod:
    """Test the main method of the cli module."""

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
