"""Test the methods of the Projects module."""

import pytest
import json
from pytest_mock import mocker
from pathlib import Path

from next_task.services import projects
from next_task.services import store


class TestKeyGenerator:
    """Test the method of the Key Generation class."""

    def test_when_provided_a_string_a_key_is_returned(self):
        """R-BICEP: Right."""
        file_data = projects.GetTasks().file_data
        assert projects.KeyGenerator("A Test Key", file_data).id == "ATK"

    def test_when_provided_an_integer_a_key_is_returned(self):
        """R-BICEP: Boundary."""
        file_data = projects.GetTasks().file_data
        assert projects.KeyGenerator(500, file_data).id == "5"


class TestCreateProject:
    """Test the method of the Project Creation class."""

    @pytest.fixture
    def mock_task_file(self, mocker) -> None:
        """Return a mock task file."""
        def mock_file_path():
            return "tests/data_mocks/task_file"
        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_that_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject("A Test Project")
        assert test_call.file_data["projects"][0]["id"] == "ATP"

    def test_when_int_is_provided_as_project_summary_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject(500).file_data["projects"][0]
        assert test_call["id"] == "5"
        assert test_call["summary"] == "500"

    def test_when_project_summary_exists_in_file_then_sys_exit(
        self,
        capsys,
        mock_task_file
    ):
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            projects.CreateProject("A Test Project")
        captured = capsys.readouterr()
        assert "Project by that name exists" in captured.out


class TestFindProjectId:
    """Test the method of the Find Project class."""

    @pytest.fixture
    def mock_task_file(self, mocker) -> None:
        """Return a mock task file."""
        def mock_file_path():
            return "tests/data_mocks/task_file"
        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_when_project_id_exists_then_found_is_true(self, mock_task_file):
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectId("ATP", data).found is True

    def test_when_project_id_case_is_wrong_then_found_is_true(
        self,
        mock_task_file
    ):
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectId("atp", data).found is True

    def test_when_provided_id_is_int_then_search_executes_and_found_is_false(
        self,
        mock_task_file
    ):
        """R-BICEP: Boundary."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectId(5, data).found is True


class TestFindProjectName:
    """Test the method of the Find Project class."""

    @pytest.fixture
    def mock_task_file(self, mocker) -> None:
        """Return a mock task file."""
        def mock_file_path():
            return "tests/data_mocks/task_file"
        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    def test_when_project_id_exists_then_found_is_true(self, mock_task_file):
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectName("A Test Project.", data).found is True

    def test_when_project_id_case_is_wrong_then_found_is_true(
        self,
        mock_task_file
    ):
        """R-BICEP: Right."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectName("a test project.", data).found is True

    def test_when_provided_id_is_int_then_search_executes_and_found_is_false(
        self,
        mock_task_file
    ):
        """R-BICEP: Boundary."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        assert projects.FindProjectName(500, data).found is True

    def test_when_additional_non_alphnum_characters_then_found_is_true(
        self,
        mock_task_file
    ):
        """R-BICEP: Boundary."""
        with open("tests/data_mocks/task_file/.tasks.json", "r") as file:
            data = json.load(file)
        test_name = "_a* Test ?project&^."
        assert projects.FindProjectName(test_name, data).found is True


class TestCreateTask:
    """Test the methods of the Create Task class."""

    @pytest.fixture(autouse=True)
    def mock_task_file(self, mocker) -> None:
        """Return a mock task file."""
        def mock_file_path():
            return "tests/data_mocks/task_file"
        mocker.patch.object(
            Path,
            "home",
            return_value=mock_file_path()
        )

    @pytest.fixture(autouse=True)
    def mock_write(self, mocker) -> None:
        """Mock the writer class."""
        mocker.patch.object(store, "WriteTask")

    def test_when_provided_project_doesnt_exist_then_sys_exit(
        self,
        capsys,
        mock_write
    ):
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            projects.CreateTask("Not a project", "A new task")
        captured = capsys.readouterr()
        assert "project Not a project not found in task file." in captured.out

    def test_when_project_id_exists_then_data_contains_project_data(
        self,
        capsys,
        mock_write
    ):
        """R-BICEP: Right."""
        test_call = projects.CreateTask("ATP", "A new task")
        assert test_call.data["id"] == "ATP"
        assert test_call.file_data["projects"][1]["task_count"] == 3

    def test_when_task_summary_is_int_then_task_is_created(
        self,
        capsys,
        mock_write
    ):
        """R-BICEP: Right."""
        test_call = projects.CreateTask("a test project", 500)
        print(test_call.file_data["projects"][1])
        assert test_call.data["id"] == "ATP"
        assert test_call.file_data["projects"][1]["task_count"] == 3


class TestGetNextTaskFromProject:
    """Test the methods that return the next task to the console."""

    def test_when_valid_requirements_then_next_task_found(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
        projects.GetNextTaskFromProject("ATP")
        captured = capsys.readouterr()
        assert "ATP-1: Test task" in captured.out

    def test_when_no_tasks_in_project_then_congratulations(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            projects.GetNextTaskFromProject("500")
        captured = capsys.readouterr()
        assert "Congratulations!" in captured.out


class TestSkipNextTaskInProject:
    """Test the method of the skip next task in project class."""

    def test_when_called_next_task_is_skipped(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
        projects.SkipNextTaskInProject("ATP")
        captured = capsys.readouterr()
        assert "ATP-2" in captured.out


class TestSkipNextTaskInProject:
    """Test the method of the skip next task in project class."""

    def test_when_called_next_task_is_closed(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
        projects.CloseNextTaskInProject("ATP")
        captured = capsys.readouterr()
        assert "ATP-2" in captured.out
