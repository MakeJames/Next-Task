"""Module containing the shared processing methods."""

import json
import sys
from datetime import datetime

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


class GetPriority:
    """Return the next priority task."""

    def __init__(self, task_data):
        """Instansiate the class."""
        logger.info("calculating task list priority")
        self.data = task_data
        self.data["tasks"].sort(key=self.calculate)

    def calculate(self, item):
        """Compound function of the due date and created date."""
        # TODO: priority should be inherited from project
        created = datetime.strptime(item["created"],
                                    "%Y-%m-%d %H:%M:%S").timestamp()
        due = datetime.strptime(item["due"],
                                "%Y-%m-%d %H:%M:%S").timestamp()
        call = created * (due - created) * 0.6
        return call


class CheckTasks:
    """Check the formatting and reformat file to valid data structure."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        logger.debug("Checking formating of the task array")

        if type(self.data) is not dict:
            logger.warning("Data is is not an dictionary, "
                           "correcting data integrity error")
            self.data = store.LoadTemplate().data

        if self.data == {}:
            logger.warning("Data is empty, correcting "
                           "data integrity error")
            self.data = store.LoadTemplate().data

        if "tasks" not in self.data:
            logger.warning("Key missing from file, "
                           "correcting data integrity error")
            self.data = store.LoadTemplate().data

        if type(self.data["tasks"]) is not list:
            logger.warning("Key missing from file, "
                           "correcting data integrity error")
            self.data = store.LoadTemplate().data


class CheckTaskCount:
    """Check the presence of a task count."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        logger.debug("checking task count field")
        if "task_count" not in self.data:
            logger.warning("task_count not in data, calculating task count")
            self.data["task_count"] = FetchLastId(self.data).id
            logger.debug(f"task_count {self.data['task_count']}")


class CheckCompleted:
    """Check the presence of a Completed task list."""

    def __init__(self, data):
        """Instansiate the class."""
        logger.debug("Checking completed_tasks")
        self.data = data
        if "completed_tasks" not in self.data:
            logger.info("Reformating tasks and extracting completed tasks")
            completed = []
            open_tasks = []
            for item in self.data["tasks"]:
                if item["status"] == "closed":
                    logger.debug(f"Removing task {item['id']} from tasks")
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
        self.data = CheckCompleted(self.data).data
        self.data = CheckTaskCount(self.data).data
