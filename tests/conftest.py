"""Instansiate project pytest fixtures."""

import pytest
import pytest_mock
from pytest_mock import mocker

from pathlib import Path

@pytest.fixture(autouse=True)
def mock_pathlib_home(tmpdir, mocker):
    """Create a mocked temp directory."""
    def home_directory():
        return tmpdir
    mocker.patch.object(Path, "home", return_value=home_directory())
