"""Module containing methods and classes for parsing projects."""

import datetime

from next_task.interface import console_output
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
        self.summary = summary
        self.file_data = GetTasks().file_data
        self.project_formatter()
        WriteTask(self.file_data)
        # console_output.Format(self.project).create_project()

    def project_formatter(self):
        """Build the project dictionary."""
        self.project = {
            "id": KeyGenerator(self.summary).id,
            "summary": str(self.summary),
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_count": 0,
            "tasks": [],
            "closed": []
        }
        self.file_data["projects"].append(self.project)
