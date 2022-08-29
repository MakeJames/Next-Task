"""Service module containing methods relating to the task file."""

import json
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path

from rich import print

from next_task.services import models


class CheckTasks:
    """Check the formatting and reformat file to valid data structure."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data

        if type(self.data) is not dict:
            print("[red]Data is is not a dictionary, "
                  "correcting data integrity error[/red]")
            self.data = models.TemplateTaskFile().__dict__

        if self.data == {}:
            print("[red]Data is empty, correcting "
                  "data integrity error[/red]")
            self.data = models.TemplateTaskFile().__dict__

        if "tasks" not in self.data:
            print("[red]Key missing from file, "
                  "correcting data integrity error[/red]")
            self.data = models.TemplateTaskFile().__dict__

        if type(self.data["tasks"]) is not list:
            print("[red]Key missing from file, "
                  "correcting data integrity error[/red]")
            self.data = models.TemplateTaskFile().__dict__


class CheckTaskCount:
    """Check the presence of a task count."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "task_count" not in self.data:
            self.fetch_id()
            self.data["task_count"] = self.id

    def fetch_id(self):
        """Return the id of the last task."""
        if self.data["tasks"] == [] \
           and self.data["completed"]["tasks"] == []:
            self.id = 0
            return

        self.id = len(self.data["tasks"]) \
            + len(self.data["completed"]["tasks"])


class CheckCompleted:
    """Check the presence of a Completed task list."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "completed" not in self.data:
            completed = []
            open_tasks = []
            for item in self.data["tasks"]:
                if item["status"] == "closed":
                    completed.append(item)
                    continue

                open_tasks.append(item)

            self.data["tasks"] = open_tasks
            self.data["completed"] = {}
            self.data["completed"]["tasks"] = completed

        # Legacy compatability, ensures pre-0.3.8 task files are formatted
        if "completed_tasks" in self.data:
            self.data["completed"] = {}
            self.data["completed"]["tasks"] = self.data["completed_tasks"]
            self.data.pop("completed_tasks")

        if "projects" not in self.data["completed"]:
            self.data["completed"]["projects"] = []


class CheckCurrent:
    """Ensure that there is a current key in the file."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "current" not in self.data:
            self.data["current"] = {}

        if "task" not in self.data["current"]:
            self.data["current"]["task"] = {}

        if "project" not in self.data["current"]:
            self.data["current"]["project"] = {}


class CheckProjects:
    """Ensure that there is a project key in the file."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "projects" not in self.data:
            self.data["projects"] = []


class CheckFormatting:
    """Ensure File data model conforms."""

    def __init__(self, data):
        """Validate that .tasks.json file meets the expected format."""
        self.data = data
        self.data = CheckTasks(self.data).data
        self.data = CheckCompleted(self.data).data
        self.data = CheckTaskCount(self.data).data
        self.data = CheckCurrent(self.data).data
        self.data = CheckProjects(self.data).data


class CheckTaskStore:
    """Confirm task file exits."""

    def __init__(self):
        """Instansiate the Check class."""
        self.file = f"{str(Path.home())}/.tasks.json"
        if self.exists() is False:
            with open(self.file, "a+") as file:
                json.dump("{}", file, indent=4)

    def exists(self):
        """Check that the path exists."""
        if Path(self.file).exists():
            return True
        return False


class Tasks:
    """Opens up the task file and returns the json as a python dictionary."""

    _date_format = "%Y-%m-%d %H:%M:%S"
    _now = dt.now()
    now = _now.strftime(_date_format)
    due = (_now+timedelta(days=7)).strftime(_date_format)

    def __init__(self):
        """Instansiate the class."""
        with open(CheckTaskStore().file, "r+") as file:
            self.file_data = json.load(file)
        self.file_data = CheckFormatting(self.file_data).data
        self.current_task = self.file_data["current"]["task"]
        self.current_project = self.file_data["current"]["project"]
        self.tasks = self.file_data["tasks"]
        self.projects = self.file_data["projects"]
        self.task_count = self.file_data["task_count"]
        self.completed_tasks = self.file_data["completed"]["tasks"]
        self.completed_projects = self.file_data["completed"]["projects"]


class WriteTask:
    """Write to .tasks.json."""

    def __init__(self, data):
        """Instansiate the Write Class."""
        self.file = CheckTaskStore().file
        if isinstance(data, dict):
            self.data = CheckFormatting(data).data
        else:
            self.data = self.format_task_file_data(data)

        with open(self.file, "w+") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)

    def format_task_file_data(self, task_data):
        """Map the Task data to a python dictionary."""
        return {
            "current": {
                "task": task_data.current_task,
                "project": task_data.current_project
            },
            "task_count": task_data.task_count,
            "tasks": task_data.tasks,
            "projects": task_data.projects,
            "completed": {
                "tasks": task_data.completed_tasks,
                "projects": task_data.completed_projects
            },
            "last_updated": task_data.now
        }
