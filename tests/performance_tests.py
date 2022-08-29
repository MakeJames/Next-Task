"""Benchmark tests against create, skip and close."""

import pytest
from pathlib import Path
from next_task.services import store
from next_task.services import tasks

@pytest.fixture
def mock_write(mocker):
    """Mock the write function."""
    def mock_function():
        return None
    mocker.patch.object(
        store.WriteTask,
        "__init__",
        return_value=mock_function()
    )

@pytest.fixture
def mock_file_path(mocker):
    """Mock task file."""

    def mock_file_path():
        return "tests/data_mocks/performance_small"

    mocker.patch.object(
        Path,
        "home",
        return_value=mock_file_path()
    )

@pytest.fixture
def mock_large_file_path(mocker):
    """Mock task file."""

    def mock_file_path():
        return "tests/data_mocks/task_file"

    mocker.patch.object(
        Path,
        "home",
        return_value=mock_file_path()
    )


def mimic_user():
    """A script to walk through several of the user functions."""
    tasks.CreateTask(0, "A task")
    tasks.CreateTask(1, "Another task")
    tasks.GetNextTask().print_task()
    tasks.SkipTask()
    tasks.MarkAsClosed()
    tasks.GetNextTask().print_task()
    tasks.MarkAsClosed()
    tasks.CreateTask(2, "Yet more Further work")
    tasks.GetNextTask().print_task()
    tasks.MarkAsClosed()


def test_create_task(benchmark):
    """R-BICEP: Performance."""
    benchmark.pedantic(tasks.CreateTask, args=(0, "this is a task",), iterations=10, rounds=100)

def test_skip_task(mock_write, mock_file_path, benchmark):
    """R-BICEP: Performance."""
    benchmark.pedantic(tasks.SkipTask, iterations=10, rounds=100)

def test_complete_task(mock_write, mock_large_file_path, benchmark):
    benchmark.pedantic(tasks.MarkAsClosed, iterations=90, rounds=100)

def test_user_behavior(benchmark):
    """R-BICEP: Performance."""
    benchmark.pedantic(mimic_user, iterations=10, rounds=20)
