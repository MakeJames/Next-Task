"""Test the methods of the controller module."""

import json
import pytest

from pytest_mock import mocker

from next_task.interface import controller


class TestArguments:
    """Test the methods of the arguments class."""

    def test_when_add_and_done_then_exit(self):
        """R-BICEP: Boundary."""
        add_done = {
            "add": "add_task",
            "task": False,
            "skip": False,
            "done": True,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**add_done)
        assert test.action is None

    def test_when_add_and_skip_then_exit(self):
        """R-BICEP: Boundary."""
        add_skip = {
            "add": "add_task",
            "task": False,
            "skip": True,
            "done": False,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**add_skip)
        assert test.action is None

    def test_when_skip_and_done_then_exit(self):
        """R-BICEP: Boundary."""
        skip_done = {
            "add": None,
            "task": False,
            "skip": True,
            "done": True,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**skip_done)
        assert test.action is None

    def test_task_options(self):
        """R-BICEP: Right."""
        # Create task
        call = {
            "add": "A task",
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "create task"
        # Create second task to avoid removal error
        call = {
            "add": "A 2nd task",
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "create task"
        # Get task
        call = {
            "add": None,
            "task": True,
            "skip": False,
            "done": False,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "get task"
        # List tasks
        call = {
            "add": None,
            "task": False,
            "skip": False,
            "done": False,
            "list": True,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "list task"
        # Skip task
        call = {
            "add": None,
            "task": False,
            "skip": True,
            "done": False,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "skip task"
        # Close task
        call = {
            "add": None,
            "task": False,
            "skip": False,
            "done": True,
            "list": False,
            "project": None
        }
        test = controller.Arguments(**call)
        assert test.action == "close task"

    def test_project_options(self):
        """R-BICEP: Right."""
        call = {
            "add": "A project",
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": True
        }
        test = controller.Arguments(**call)
        assert test.action == "create project"
        call = {
            "add": None,
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": True
        }
        test = controller.Arguments(**call)
        assert test.action == "list projects"

        call = {
            "add": "A task",
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project add task"

        call = {
            "add": "A 2nd task",
            "task": False,
            "skip": False,
            "done": False,
            "list": False,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project add task"

        call = {
            "add": None,
            "task": True,
            "skip": False,
            "done": False,
            "list": False,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project get task"

        call = {
            "add": None,
            "task": False,
            "skip": False,
            "done": False,
            "list": True,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project list tasks"

        call = {
            "add": None,
            "task": False,
            "skip": True,
            "done": False,
            "list": False,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project skip task"

        call = {
            "add": None,
            "task": False,
            "skip": False,
            "done": True,
            "list": False,
            "project": "AP"
        }
        test = controller.Arguments(**call)
        assert test.action == "project close task"

        call = {
            "add": "A task",
            "task": True,
            "skip": False,
            "done": False,
            "list": False,
            "project": True
        }
        test = controller.Arguments(**call)
        assert test.action is None
