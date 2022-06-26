"""Service module containing methods relating to the task file."""

import json
from os import path
from pathlib import Path

from rich import print


class LoadTemplate:
    """Load the template file."""

    def __init__(self):
        """Instansiate the class."""
        with open(path.join(path.dirname(__file__), "template.json"),
                  "r") as file:
            self.data = json.load(file)


class CheckTasks:
    """Check the formatting and reformat file to valid data structure."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data

        if type(self.data) is not dict:
            print("[red]Data is is not an dictionary, "
                  "correcting data integrity error[/red]")
            self.data = LoadTemplate().data

        if self.data == {}:
            print("[red]Data is empty, correcting "
                  "data integrity error[/red]")
            self.data = LoadTemplate().data

        if "tasks" not in self.data:
            print("[red]Key missing from file, "
                  "correcting data integrity error[/red]")
            self.data = LoadTemplate().data

        if type(self.data["tasks"]) is not list:
            print("[red]Key missing from file, "
                  "correcting data integrity error[/red]")
            self.data = LoadTemplate().data


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
           and self.data["completed_tasks"] == []:
            self.id = 0
            return

        self.id = len(self.data["tasks"]) \
            + len(self.data["completed_tasks"])


class CheckCompleted:
    """Check the presence of a Completed task list."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "completed_tasks" not in self.data:
            completed = []
            open_tasks = []
            for item in self.data["tasks"]:
                if item["status"] == "closed":
                    completed.append(item)
                    continue

                open_tasks.append(item)

            self.data["tasks"] = open_tasks
            self.data["completed_tasks"] = completed


class CheckFormatting:
    """Ensure File data model conforms."""

    def __init__(self, data):
        """Validate that .tasks.json file meets the expected format."""
        self.data = data
        self.data = CheckTasks(self.data).data
        self.data = CheckCompleted(self.data).data
        self.data = CheckTaskCount(self.data).data


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


class GetTasks:
    """Opens up the task file and returns the json as a python dictionary."""

    def __init__(self):
        """Instansiate the class."""
        with open(CheckTaskStore().file, "r") as file:
            self.file_data = json.load(file)
        self.file_data = CheckFormatting(self.file_data).data


class WriteTask:
    """Write to .tasks.json."""

    def __init__(self, data: dict):
        """Instansiate the Write Class."""
        self.file = CheckTaskStore().file
        self.data = CheckFormatting(data).data
        with open(self.file, "r+") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)
