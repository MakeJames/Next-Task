"""Instansiate project pytest fixtures."""

import sqlite3
import pytest
import pytest_mock
from pytest_mock import mocker

import next_task
from pathlib import Path
from next_task.services import database
from next_task.services.tasks import GetNextTask


@pytest.fixture
def mock_read(request, mocker):
    """Mock the read functions."""
    first = request.param
    try:
        second = [request.param[1], request.param[0]]
    except:
        second = None
    print(second)
    def mock_1():
        return first
    def mock_2():
        return second
    mocker.patch.object(database.Database, "read", side_effect=[mock_1(), mock_2()])

@pytest.fixture
def mock_write(mocker):
    """Mock the read functions."""
    def mock(self, sql):
        return 1
    mocker.patch.object(database.Database, "write", mock)

@pytest.fixture(autouse=True)
def mock_database(mocker, tmpdir):
    """Set Home directory as a temp directory."""
    class mock_db:
        def __init__(self):
            self._file = f"{tmpdir}/task.db"
    mocker.patch.object(database.Connection, "__init__", mock_db.__init__)

@pytest.fixture
def empty_db(mock_database):
    """Set Home directory as a temp directory."""
    database.Setup().create_database()


@pytest.fixture
def test_db(mock_database):
    """Set Home directory as a temp directory."""
    database.Setup().create_database()
    setup_file = "tests/database/simple_db.sql"
    with database.Connection() as conn, open(setup_file, "r") as file:
        conn.curs.executescript(file.read())

@pytest.fixture
def mock_next_task(mocker):
    """Mock the call to return the next task."""
    class mock:
        def __init__(self):
            self.task = [{
                "task_id": 430,
                "summary": "A mocked test task" 
            },]
    mocker.patch.object(GetNextTask, "__init__", mock.__init__)

@pytest.fixture
def mock_no_next_task(mocker):
    """Mock the call to return the next task."""
    class mock:
        def __init__(self):
            self.task = []
    mocker.patch.object(GetNextTask, "__init__", mock.__init__)
