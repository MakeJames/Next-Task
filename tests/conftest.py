"""Instansiate project pytest fixtures."""

import sqlite3
import pytest
import pytest_mock
from pytest_mock import mocker

from pathlib import Path
from next_task.database import store


@pytest.fixture(autouse=True, scope="function")
def empty_db(mocker):
    """Set Home directory as a temp directory."""
    class MockDatabase:
        def __init__(self):
            self._file = ":memory:"
    
        def __enter__(self):
            self.conn = sqlite3.connect(self._file)
            self.curs = self.conn.cursor()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_val:
                self.conn.close()
                # return falsy to raise exc_val
            else:
                # commit ommited to preserve database
                self.conn.close()

    mocker.patch.object(store, "Database", MockDatabase)

@pytest.fixture
def test_db(mocker):
    """Set Home directory as a temp directory."""
    class MockDatabase:
        def __init__(self):
            self._file = "tests/database/test.db"
    
        def __enter__(self):
            self.conn = sqlite3.connect(self._file)
            self.curs = self.conn.cursor()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_val:
                self.conn.close()
                # return falsy to raise exc_val
            else:
                self.conn.commit()
                self.conn.close()

    mocker.patch.object(store, "Database", MockDatabase)

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
