"""Test the methods of the Projects module."""

from multiprocessing.sharedctypes import Value
import pytest
import json
from pytest_mock import mocker
from pathlib import Path

from next_task.services import projects


class TestKeyGenerator:
    """Test the method of the Key Generation class."""

    def test_when_provided_a_string_a_key_is_returned(self) -> None:
        """R-BICEP: Right."""
        assert projects.KeyGenerator("A Test Key").id == "ATK"

    def test_when_provided_an_integer_a_key_is_returned(self) -> None:
        """R-BICEP: Boundary."""
        assert projects.KeyGenerator(500).id == "5"

    def test_when_provided_project_key_exists_then_print_error(self) -> None:
        """R-BICEP: Right."""
        assert projects.KeyGenerator("A Test Key").id == "ATK"

    def test_when_provided_empty_input_then_id_error(self) -> None:
        """R-BICEP: Boundary."""
        with pytest.raises(SyntaxError):
            test = projects.KeyGenerator("")


class TestCreateProject:
    """Test the method of the Project Creation class."""

    def test_that_project_is_created(self) -> None:
        """R-BICEP: Right."""
        class test_data:
            add = "A Test Project"
            projects = [{"id": "AP", "summary": "Another Project"}]
            now = "2022-08-31 09:20:37"

        test_call = projects.CreateProject(test_data())
        assert test_call.id == "ATP" and test_call.summary == "A Test Project"

    def test_when_inputs_are_none_type_then_error(self) -> None:
        """R-BICEP: Boundary."""
        class test_data:
            add = None
            projects = None
            now = None
        with pytest.raises(ValueError):
            projects.CreateProject(test_data())

    def test_when_int_is_provided_project_is_created(self) -> None:
        """R-BICEP: Right."""
        class test_data:
            add = 500
            projects = [{"id": "AP", "summary": "Another Project"}]
            now = "2022-08-31 09:20:37"

        test_call = projects.CreateProject(test_data())
        assert test_call.id == "5" and test_call.summary == "500"

    def test_when_returned_class_dict_matches_expected_format(self) -> None:
        """R-BICEP: Right."""
        class test_data:
            projects = []
            add = "A Test Key"
            now = "2022-08-31 09:20:37"
        expected = {
            "id": "ATK",
            "summary": "A Test Key",
            "created": "2022-08-31 09:20:37",
            "task_count": 0,
            "tasks": [],
            "completed": {"tasks": []}
        }
        test_call = projects.CreateProject(test_data())
        assert test_call.__dict__ == expected


class TestFindProjectId:
    """Test the method of the Find Project class."""

    def test_when_project_exists_then_found_is_true(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        assert projects.FindProjectId("ATP", project_list).found is True

    def test_when_project_exists_then_data_matches_input_project(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        test = projects.FindProjectId("ATP", project_list)
        assert test.data is project_list[0]

    def test_when_id_case_is_wrong_then_found_is_true(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        assert projects.FindProjectId("atp", project_list).found is True

    def test_when_id_is_int_then_found_is_true(self) -> None:
        """R-BICEP: Boundary."""
        project_list = [{"id": "5"}]
        assert projects.FindProjectId(5, project_list).found is True

    def test_when_id_is_not_in_list_then_found_is_false(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        test_id = "XYZ"
        test_call = projects.FindProjectId(test_id, project_list)
        assert test_call.found is False

    def test_when_id_is_not_in_list_then_error(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        test_id = "XYZ"
        with pytest.raises(AttributeError):
            projects.FindProjectId(test_id, project_list).data

    def test_when_id_is_empty_then_found_is_false(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"id": "ATP"}]
        test_id = ""
        test_call = projects.FindProjectId(test_id, project_list)
        assert test_call.found is False

    def test_when_id_is_None_type_then_found_is_false(self) -> None:
        """R-BICEP: Boundary."""
        project_list = [{"id": "ATP"}]
        test_id = None
        test_call = projects.FindProjectId(test_id, project_list)
        assert test_call.found is False


class TestFindProjectName:
    """Test the method of the Find Project class."""

    def test_when_project_id_exists_then_found_is_true(self,):
        """R-BICEP: Right."""
        project_list = [{"summary": "A Test Project."}]
        test_call = projects.FindProjectName("A Test Project.", project_list)
        assert test_call.found is True

    def test_when_project_id_case_is_wrong_then_found_is_true(
        self,
    ):
        """R-BICEP: Right."""
        project_list = [{"summary": "A Test Project."}]
        test_call = projects.FindProjectName("a test project.", project_list)
        assert test_call.found is True

    def test_when_summary_is_int_then_found_is_true(
        self,
    ):
        """R-BICEP: Boundary."""
        project_list = [{"summary": "500"}]
        test_call = projects.FindProjectName(500, project_list)
        assert test_call.found is True

    def test_when_additional_non_alphnum_characters_then_found_is_true(
        self,
    ):
        """R-BICEP: Boundary."""
        project_list = [{"summary": "A Test Project."}]
        test_name = "_a* Test ?project&^."
        test_call = projects.FindProjectName(test_name, project_list)
        assert test_call.found is True

    def test_when_summary_is_not_in_list_then_found_is_false(self) -> None:
        """R-BICEP: Right."""
        project_list = [{"summary": "A Test Project."}]
        test_name = "A different project"
        test_call = projects.FindProjectName(test_name, project_list)
        assert test_call.found is False


class TestCreateTask:
    """Test the methods of the Create Task class."""

    def test_when_provided_project_doesnt_exist_then_sys_exit(
        self,
        capsys,
        mock_write,
        test_data_mock
    ):
        """R-BICEP: Right."""
        # TODO: Is this right functionality: should prompt project creation
        with pytest.raises(SystemExit):
            projects.CreateProjectTask("Not a project", "A new task",
                                       test_data_mock)
        captured = capsys.readouterr()
        assert "project Not a project not found in task file." in captured.out

    def test_when_project_id_exists_then_data_contains_project_data(
        self, mocker,
        mock_write,
        test_data_mock
    ):
        """R-BICEP: Right."""
        test_call = projects.CreateProjectTask("ATP", "A new task",
                                               test_data_mock)
        assert test_call.project_data["id"] == "ATP" \
            and test_call.file_data.projects[-1]["task_count"] == 3

    def test_when_task_summary_is_int_then_task_is_created(
        self,
        mock_write,
        test_data_mock
    ):
        """R-BICEP: Right."""
        test_call = projects.CreateProjectTask("a test project", 500,
                                               test_data_mock)
        assert test_call.project_data["id"] == "ATP" \
            and test_call.file_data.projects[-1]["task_count"] == 3


class TestGetNextTaskFromProject:
    """Test the methods that return the next task to the console."""

    def test_when_valid_requirements_then_next_task_found(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
        test = projects.GetNextTaskFromProject("ATP")
        captured = capsys.readouterr()
        assert test.file_data.current_task["id"] == "ATP-1"
        assert "ATP-1: Test task" in captured.out

    def test_when_no_tasks_in_project_then_congratulations(
        self,
        capsys,
        mock_write,
        mock_task_file
    ):
        """R-BICEP: Right."""
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
