"""Instansiate project pytest fixtures."""

import sqlite3
import pytest
import pytest_mock
from pytest_mock import mocker

from pathlib import Path
from next_task.database import store


@pytest.fixture(autouse=True)
def mock_home_directory_as_tmpdir(tmpdir, mocker):
    """Set Home directory as a temp directory."""
    class mock_database:
        def __init__(self):
            self._version = 0.1
            self._folder = f"{tmpdir}/Notes/nextTask"
            self._file = f"{self._folder}/task.db"
    mocker.patch.object(store, "Database", mock_database)

@pytest.fixture
def mock_sqlite(mocker):
    """Mock the Sqlite library to prevent database creation."""
    mocker.patch.object(sqlite3, "connect")
    mocker.patch.object(store.Check, "database_version_is_latest",
                        return_value=True)

@pytest.fixture
def mock_task_file(mocker) -> None:
    """Return a mock task file."""
    def mock_file_path():
        return "tests/data_mocks/task_file"
    mocker.patch.object(
        Path,
        "home",
        return_value=mock_file_path()
    )
