"""Module containing methods and classes for parsing projects."""

import re
import sys
from datetime import datetime as dt

from next_task.interface.console_output import Format, FormatProject
from next_task.services.models import Project, Task
from next_task.services.store import GetTasks, WriteTask
from next_task.services.tasks import GetNextTask, MarkAsClosed, SkipTask


class KeyGenerator:
    """Generate a project stub."""

    def __init__(self, summary, file_data):
        """Instansiate the Key Generator Class."""
        self.generate_key(summary)
        if FindProjectId(id=self.id, data=file_data).found:
            print(f"{self.id}: in project list.")

    def generate_key(self, string):
        """Generate the project key."""
        words = str(string).split()[:3]
        self.id = ""
        for word in words:
            self.id += word[0].upper()


class CreateProject:
    """Create a new Project."""

    def __init__(self, summary):
        """Instanisate the Create project class."""
        self.file_data = GetTasks().file_data
        if FindProjectName(summary, data=self.file_data).found:
            print("Project by that name exists.")
            sys.exit([0])
        self.project_formatter(summary, self.file_data)
        WriteTask(self.file_data)
        FormatProject(self.project).create()

    def project_formatter(self, summary, file_data):
        """Build the project dictionary."""
        self.project = Project(KeyGenerator(summary, file_data).id,
                               summary, dt.now()).__dict__
        self.file_data["projects"].append(self.project)


class FindProjectId:
    """Search for a project by id in a given list of projects."""

    def __init__(self, id, data):
        """Instansiate the class."""
        for item in data["projects"]:
            if item["id"] == str(id).upper():
                self.data = item
                self.found = True
                return
        self.found = False
        self.data = {}


class FindProjectName:
    """Search for a project by summary in a given list of projects."""

    def __init__(self, summary, data):
        """Instansiate the class."""
        summary = re.sub(r'[^a-zA-Z0-9]', '', str(summary))
        for item in data["projects"]:
            item_summary = re.sub(r'[^a-zA-Z0-9]', '', item["summary"])
            if item_summary.lower() == str(summary).lower():
                self.data = item
                self.found = True
                return
        self.found = False
        self.data = {}


class FindProject:
    """Wrap for the Find Project by name and id class."""

    def __init__(self, summary, data):
        """Instansiate the class."""
        id = FindProjectId(summary, data)
        if id.found:
            self.data = id.data
            return

        name = FindProjectName(summary, data)
        if name.found:
            self.data = name.data
            return

        print(f"project {summary} not found in task file.")
        sys.exit([0])


class CreateProjectTask:
    """Create a task in a given project."""

    def __init__(self, project, summary):
        """Instansiate the class."""
        self.file_data = GetTasks().file_data
        self.data = FindProject(project, self.file_data).data
        self.generate_id()
        self.file_data["projects"].remove(self.data)
        self.task = Task(self.task_id, str(summary), dt.now()).__dict__
        self.data["tasks"].append(self.task)
        self.file_data["projects"].append(self.data)
        Format(self.task).create_task()
        WriteTask(self.file_data)

    def generate_id(self):
        """Generate the task id."""
        self.data["task_count"] += 1
        self.task_id = f"{self.data['id']}-{self.data['task_count']}"


class GetNextTaskFromProject:
    """Return the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        self.file_data = GetTasks().file_data
        self.data = FindProject(project, self.file_data).data
        GetNextTask(self.data).print_task()


class SkipNextTaskInProject:
    """Skip the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        self.file_data = GetTasks().file_data
        self.data = FindProject(project, self.file_data).data
        SkipTask(self.data)


class CloseNextTaskInProject:
    """Skip the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        self.file_data = GetTasks().file_data
        self.data = FindProject(project, self.file_data).data
        MarkAsClosed(self.data)
