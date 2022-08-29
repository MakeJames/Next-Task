"""Test the methods of the Projects module."""

import pytest
import json
from pytest_mock import mocker
from pathlib import Path

from next_task.services import projects
from next_task.services import store
from next_task.services import tasks
from next_task.services.tasks import TaskData


class TestKeyGenerator:
    """Test the method of the Key Generation class."""

    def test_when_provided_a_string_a_key_is_returned(self, capsys):
        """R-BICEP: Right."""
        class test_data:
            pass
        test_data.projects = []
        assert projects.KeyGenerator("A Test Key", test_data).id == "ATK" \
            and capsys.readouterr().out == ""

    def test_when_provided_an_integer_a_key_is_returned(self, capsys):
        """R-BICEP: Boundary."""
        class test_data:
            pass
        test_data.projects = []
        assert projects.KeyGenerator(500, test_data).id == "5" \
            and capsys.readouterr().out == ""

    def test_when_provided_project_key_exists_then_print_error(self, capsys):
        """R-BICEP: Right."""
        class test_data:
            pass
        test_data.projects = [{"id": "ATK"}]
        assert projects.KeyGenerator("A Test Key", test_data).id == "ATK" \
            and capsys.readouterr().out == "ATK: in project list.\n"


class TestCreateProject:
    """Test the method of the Project Creation class."""

    def test_that_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject("A Test Project")
        assert test_call.file_data.projects[0]["id"] == "ATP"

    def test_when_int_is_provided_as_project_summary_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject(500).file_data.projects[0]
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

    def test_when_project_id_exists_then_found_is_true(self):
        """R-BICEP: Right."""
        class test_data:
            projects = [{"id": "ATP"}]
        assert projects.FindProjectId("ATP", test_data).found is True

    def test_when_project_id_case_is_wrong_then_found_is_true(
        self,
    ):
        """R-BICEP: Right."""
        class test_data:
            projects = [{"id": "ATP"}]
        assert projects.FindProjectId("atp", test_data).found is True

    def test_when_provided_id_is_int_then_search_executes_and_found_is_false(
        self,
    ):
        """R-BICEP: Boundary."""
        class test_data:
            pass
        test_data.projects = [{"id": "5"}]
        assert projects.FindProjectId(5, test_data).found is True


class TestFindProjectName:
    """Test the method of the Find Project class."""

    def test_when_project_id_exists_then_found_is_true(self,):
        """R-BICEP: Right."""
        class test_data:
            projects = [{"summary": "A Test Project."}]
        test_call = projects.FindProjectName("A Test Project.", test_data)
        assert test_call.found is True

    def test_when_project_id_case_is_wrong_then_found_is_true(
        self,
    ):
        """R-BICEP: Right."""
        class test_data:
            projects = [{"summary": "A Test Project."}]
        test_call = projects.FindProjectName("a test project.", test_data)
        assert test_call.found is True

    def test_when_provided_id_is_int_then_search_executes_and_found_is_false(
        self,
    ):
        """R-BICEP: Boundary."""
        class test_data:
            projects = [{"summary": "500"}]
        test_call = projects.FindProjectName(500, test_data)
        assert test_call.found is True

    def test_when_additional_non_alphnum_characters_then_found_is_true(
        self,
    ):
        """R-BICEP: Boundary."""
        class test_data:
            projects = [{"summary": "A Test Project."}]
        test_name = "_a* Test ?project&^."
        test_call = projects.FindProjectName(test_name, test_data)
        assert test_call.found is True


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
        assert test.file_data.current["task"]["id"] == "ATP-1"
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
