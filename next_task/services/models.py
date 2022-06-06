"""Module containing the shared processing methods."""

import datetime
import json
import sys

from loguru import logger

from next_task.services import store, tasks


class FetchLastId:
    """Legacy Function to identify and return the id of the last task."""

    def __init__(self, data: dict):
        """Instansiate the class."""
        self.data = data
        self.fetch_id()

    def fetch_id(self):
        """Return the id of the last task."""
        if self.data["tasks"] == []:
            self.id = 0
        else:
            last_task = self.data["tasks"][-1]
            self.id = last_task["id"]


class FilterOpenTasks:
    """Filter for open tasks."""

    # TODO: Remove when done updates the list the task is in

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


class CheckTasks:
    """Check the formatting and reformat file to valid data structure."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data

        if type(self.data) is not dict:
            logger.warning(
                "Data is is not an dictionary, correcting data integrity error"
            )
            self.data = store.LoadTemplate().data

        if self.data == {}:
            logger.warning(
                "Data is empty, correcting data integrity error"
            )
            self.data = store.LoadTemplate().data

        if "tasks" not in self.data:
            logger.warning(
                "Key missing from file, correcting data integrity error"
            )
            self.data = store.LoadTemplate().data

        if type(self.data["tasks"]) is not list:
            logger.warning(
                "Key missing from file, correcting data integrity error"
            )
            self.data = store.LoadTemplate().data


class CheckTaskCount:
    """Check the presence of a task count."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "task_count" not in self.data:
            self.data["task_count"] = FetchLastId(self.data).id


class CheckCompleted:
    """Check the presence of a Completed task list."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        if "completed_tasks" not in self.data:
            completed = []
            open_tasks = []
            for item in self.data["tasks"]:
                logger.debug(f"Checking {item['id']}")
                if item["status"] == "closed":
                    logger.debug("Removing item from tasks")
                    completed.append(item)
                else:
                    open_tasks.append(item)

            self.data["tasks"] = open_tasks
            self.data["completed_tasks"] = completed


class CheckFormatting:
    """Read the current data model."""

    def __init__(self, data):
        """Validate that .tasks.json file meets the expected format."""
        self.data = data
        self.data = CheckTasks(self.data).data
        self.data = CheckTaskCount(self.data).data
        self.data = CheckCompleted(self.data).data
