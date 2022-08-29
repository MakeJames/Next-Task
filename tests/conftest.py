"""Instansiate project pytest fixtures."""

import pytest
import pytest_mock
from pytest_mock import mocker

from pathlib import Path
from next_task.services import store


@pytest.fixture(autouse=True)
def mock_pathlib_home(tmpdir, mocker):
    """Create a mocked temp directory."""
    def home_directory():
        return tmpdir
    mocker.patch.object(Path, "home", return_value=home_directory())

@pytest.fixture
def mock_write(mocker):
    """Mock the write aspect of the writer function."""
    def mock_function():
        return None
    mocker.patch.object(
        store.WriteTask,
        "__init__",
        return_value=mock_function()
    )

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

@pytest.fixture
def test_data_mock():
    """A mock for the TaskData class."""
    class TestData:
        tasks = []
        current = {"task": {}, "project": {}}
        completed = {"tasks": [], "projects": []}
        task_count = 20
        projects = [
            {
                "id": "ATP",
                "summary": "A Test Project.",
                "task_count": 2,
                "tasks": [
                    {
                        'id': 'ATP-1',
                        'summary': 'Test task',
                        'created': '2022-06-03 09:00:26',
                        'due': '2022-06-10 09:00:26'
                    }, 
                    {
                        'id': 'ATP-2',
                        'summary': 'Another Test task',
                        'created': '2022-06-03 09:00:26',
                        'due': '2022-06-10 09:00:26'
                    }
                ]
            },
            {
                "id": "5",
                "summary": "500",
                "task_count": 0,
                "tasks": []
            }        
        ]
    return TestData()