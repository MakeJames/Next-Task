"""Module containing methods and classes for parsing projects."""

from datetime import datetime as dt

from next_task.interface import console_output
from next_task.services.models import Project
from next_task.services.store import GetTasks, WriteTask
from next_task.services.tasks import (CreateTask, GetNextTask, MarkAsClosed,
                                      SkipTask)


class KeyGenerator:
    """Generate a project stub."""

    def __init__(self, string):
        """Instansiate the Key Generator Class."""
        words = str(string).split()[:3]
        self.id = ""
        for word in words:
            self.id += word[0]


class CreateProject:
    """Create a new Project."""

    def __init__(self, summary):
        """Instanisate the Create project class."""
        self.file_data = GetTasks().file_data
        self.project_formatter(summary)
        WriteTask(self.file_data)
        # console_output.Format(self.project).create_project()

    def project_formatter(self, summary):
        """Build the project dictionary."""
        self.project = Project(KeyGenerator(summary).id,
                               summary, dt.now()).__dict__
        self.file_data["projects"].append(self.project)
