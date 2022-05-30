"""Test the methods of the file module."""

import pytest
from loguru import logger
from pathlib import Path
from pytest_mock import mocker

from next_task.services import file


class TestCheckClass:
    """Test the methods of the Check class."""

    def test_that_mock_pathlib_is_not_home_directory(self) -> None:
        """R-BICEP: Right."""
        _file = file.Check()
        assert Path(_file.file).exists()
