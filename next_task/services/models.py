"""Module containing the shared processing methods."""

import datetime
import json
import sys

from loguru import logger

from next_task.services import store, tasks


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


class FilterOpenTasks:
    """Filter for open tasks."""

    def __init__(self, data):
        """Instansiate Filter Open Tasks class."""
        self.data = [
            item for item in data["tasks"] if item["status"] == "open"
        ]


class GetPriority:
    """Return the next priority task."""

    def __init__(self, task_data):
        """Instansiate the class."""
        self.data = task_data
        self.data.sort(key=self.calculate)

    def calculate(self, item):
        """Compound function of the due date and created date."""
        # TODO: priority should be inherited from project
        created = datetime.datetime.strptime(
            item["created"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        due = datetime.datetime.strptime(
            item["due"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        call = created * (due - created) * 0.6
        # logger.debug(f"Priority: {call}")
        return call
