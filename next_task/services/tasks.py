"""Module containing the methods relating to task creation."""

import datetime
import json
from nis import cat

from loguru import logger

from next_task.services import catalogue


class FetchLastId:
    """Identify and return the id of the last task."""

    def __init__(self, data: dict):
        """Instansiate the class."""
        self.data = data
        self.check_formating()
        self.fetch_id()

    def check_formating(self):
        """Validate that .tasks.json file meets the expected format."""
        # TODO: These errors should promt user to reformat .tasks.json
        # Consider that if an empty or formatted string gets passed in
        # then none of these checks explicitly guard against it. How
        # would this impact the reformatting of the file data
        if self.data == {}:
            raise NameError(".tasks.json not formatted.")

        if "tasks" not in self.data:
            logger.debug(self.data)
            raise KeyError("tasks not in dictonary.")

        if type(self.data["tasks"]) is not list:
            logger.debug(type(self.data["tasks"]))
            raise AttributeError(".tasks.json not formatted correctly.")

    def fetch_id(self):
        """Return the id of the last task."""
        if self.data["tasks"] == []:
            self.id = 0
        else:
            last_task = self.data["tasks"][-1]
            self.id = last_task["id"]


class CreateTask:
    """Setup class to create the structure of the json file."""

    def __init__(self, summary: str):
        """Instansiate the Write task class."""
        self.summary = summary
        self.now = datetime.datetime.now()
        self.due = (self.now + datetime.timedelta(days=7))
        self._file = open(catalogue.Check().file, "r+")
        self.file_data = json.load(self._file)
        self.id = (FetchLastId(self.file_data).id + 1)
        self.task_formatter()
        self.write()

    def task_formatter(self):
        """Build task dictionary."""
        self.data = {
            "id": self.id,
            "summary": self.summary,
            "created": self.now.strftime("%Y-%m-%d %H:%M:%S"),
            "due": self.due.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "open"
        }
        logger.debug(
            f"Creating task {self.data['id']}: {self.data['summary']}" +
            f" - {self.data['created']}"
        )

    def write(self):
        """Write the task to the task file."""
        logger.debug("writing task to .tasks.json")
        self.file_data["tasks"].append(self.data)
        self._file.seek(0)
        json.dump(self.file_data, self._file, indent=4)
        self._file.close()
        print(
            f"Created task {self.id}: {self.summary} " +
            f"- Due: {self.due.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class FilterOpenTasks:
    """Filter for open tasks."""

    def __init__(self, data):
        """Instansiate Filter Open Tasks class."""
        self.data = [
            item for item in data["tasks"] if item['status'] == 'open'
        ]


class GetPriority:
    """Return the next priority task."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        self.data.sort(key=self.calculate)
        self.task = self.data[0]
        logger.debug(f"{self.task['id']}: {self.task['summary']}")

    def calculate(self, item):
        """Compound function of the due date and created date."""
        # TODO: with a skip function, this should divide by skips
        # TODO: priority should be inherited from project
        created = datetime.datetime.strptime(
            item["created"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        due = datetime.datetime.strptime(
            item["due"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        call = created * \
            (due - created)
        return call * 0.6


class GetNextTask:
    """Print the next task to the command line."""

    def __init__(self):
        """Instansiate the get task wrapper class."""
        self._file = open(catalogue.Check().file, "r")
        self.data = json.load(self._file)
        self.open_tasks = FilterOpenTasks(self.data).data
        self.task = GetPriority(self.open_tasks).task
        self._file.close()

    def print_task(self):
        """Print the next task."""
        print(f"{self.task['id']}: {self.task['summary']}")
        print(f"due {self.task['due']}")
