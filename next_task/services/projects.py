"""Module containing methods and classes for parsing projects."""

import re
from datetime import datetime as dt

from next_task.interface.console_output import Format
from next_task.services.models import Task
from next_task.services.store import Tasks, WriteTask
from next_task.services.tasks import GetNextTask, MarkAsClosed, SkipTask


class CreateProject:
    """Model for a project."""

    def __init__(self, task_data):
        """Instansiate the Project model."""
        if None in [task_data.add, task_data.now]:
            raise ValueError
        self.id = KeyGenerator(task_data.add).id
        self.summary = str(task_data.add)
        self.created = task_data.now
        self.task_count = 0
        self.tasks = []
        self.completed = {"tasks": []}


class KeyGenerator:
    """Generate a project key."""

    def __init__(self, summary):
        """Instansiate the Key Generator Class."""
        words = str(summary).split()[:3]
        if words == []:
            raise SyntaxError("Input cannot be empty on key generation")
        self.id = ""
        for word in words:
            self.id += word[0].upper()


class FindProjectId:
    """Search for a project by id in a given list of projects."""

    def __init__(self, id, list_of_projects):
        """Instansiate the class."""
        for project in list_of_projects:
            if project["id"] == str(id).upper():
                self.data = project
                self.found = True
                return
        self.found = False


class FindProjectName:
    """Search for a project by summary in a given list of projects."""

    def __init__(self, summary, list_of_projects):
        """Instansiate the class."""
        summary = re.sub(r'[^a-zA-Z0-9]', '', str(summary))
        for project in list_of_projects:
            item_summary = re.sub(r'[^a-zA-Z0-9]', '', project["summary"])
            if item_summary.lower() == str(summary).lower():
                self.data = project
                print(self.data['summary'])
                self.found = True
                return
        self.found = False


class FindProject(FindProjectId, FindProjectName):
    """Wrap for the Find Project by name and id class."""

    def __init__(self, lookup_value, list_of_projects):
        """Instansiate the class."""
        FindProjectId.__init__(self, lookup_value, list_of_projects)
        if self.found:
            return
        FindProjectName.__init__(self, lookup_value, list_of_projects)
        if self.found:
            return
        self.data = None


class CreateProjectTask:
    """Create a task in a given project."""

    def __init__(self, project, summary, task_data):
        """Instansiate the class."""
        # TODO: this is uncessiarily complicated - FIX
        self.file_data = task_data
        self.project_data = FindProject(project, task_data).data
        self.generate_id()
        self.file_data.projects.remove(self.project_data)
        self.task = Task(self.task_id, str(summary), dt.now()).__dict__
        self.project_data["tasks"].append(self.task)
        self.file_data.projects.append(self.project_data)
        Format(self.task).create_task()
        WriteTask(self.file_data)

    def generate_id(self):
        """Generate the task id."""
        self.project_data["task_count"] += 1
        self.task_id = f"{self.project_data['id']}" \
                       f"-{self.project_data['task_count']}"


class GetNextTaskFromProject:
    """Return the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        # TODO: this is uncessiarily complicated - FIX
        # FIX: Method does not access Project tasks
        self.file_data = Tasks()
        task_data = self.file_data.tasks
        self.project_data = FindProject(project, self.file_data).data
        self.file_data.tasks = self.project_data["tasks"]
        self.file_data.projects.remove(self.project_data)
        self.file_data = GetNextTask(self.file_data).task_data
        self.project_data["tasks"] = self.file_data.tasks
        self.file_data.projects.append(self.project_data)
        self.file_data.tasks = task_data
        if self.file_data.current_task:
            Format(self.file_data.current_task).next_task()
        WriteTask(self.file_data.__dict__)


class SkipNextTaskInProject:
    """Skip the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        # TODO: this is uncessiarily complicated - FIX
        # FIX: Method does not access Project tasks
        self.file_data = Tasks()
        task_data = self.file_data.tasks
        self.project_data = FindProject(project, self.file_data).data
        self.file_data.tasks = self.project_data["tasks"]
        self.file_data.projects.remove(self.project_data)
        self.file_data = GetNextTask(self.file_data).task_data
        skip = SkipTask(self.file_data)
        self.file_data = GetNextTask(skip.task_data).task_data
        self.project_data["tasks"] = self.file_data.tasks
        self.file_data.projects.append(self.project_data)
        self.file_data.tasks = task_data
        Format(skip.skip_task).skip_task()
        WriteTask(self.file_data)


class CloseNextTaskInProject:
    """Skip the next Task in a project."""

    def __init__(self, project):
        """Instansiate class."""
        # TODO: this is uncessiarily complicated - FIX
        # FIX: Method does not access Project tasks
        self.file_data = Tasks()
        task_data = self.file_data.tasks
        self.project_data = FindProject(project, self.file_data).data
        self.file_data.tasks = self.project_data["tasks"]
        self.file_data.projects.remove(self.project_data)
        self.file_data = GetNextTask(self.file_data).task_data
        close = MarkAsClosed(self.file_data)
        self.file_data = GetNextTask(close.task_data).task_data
        self.project_data["tasks"] = self.file_data.tasks
        self.file_data.projects.append(self.project_data)
        self.file_data.tasks = task_data
        Format(close.closed_task).mark_closed()
        Format(self.file_data.current_task).next_task()
        WriteTask(self.file_data.__dict__)
