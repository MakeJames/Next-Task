"""Test the methods of the Projects module."""

import pytest
import json
from pytest_mock import mocker
from pathlib import Path

from next_task.services import projects


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
