"""Test the methods of the Projects module."""

import pytest
import json
from pytest_mock import mocker

from next_task.services import projects


class TestKeyGenerator:
    """Test the method of the Key Generation class."""

    def test_when_provided_a_string_a_key_is_returned(self):
        """R-BICEP: Right."""
        assert projects.KeyGenerator("A Test Key").id == "ATK"

    def test_when_provided_an_integer_a_key_is_returned(self):
        """R-BICEP: Boundary."""
        assert projects.KeyGenerator(500).id == "5"


class TestCreateProject:
    """Test the method of the Project Creation class."""

    def test_that_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject("A Test Project")
        assert test_call.file_data["projects"][0]["id"] == "ATP"

    def test_when_int_is_provided_as_project_summary_project_is_created(self):
        """R-BICEP: Right."""
        test_call = projects.CreateProject(500).file_data["projects"][0]
        assert test_call["id"] == "5"
        assert test_call["summary"] == "500"
