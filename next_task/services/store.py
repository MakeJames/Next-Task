"""Service module containing methods relating to the task file."""

import json
import sys
from pathlib import Path

from loguru import logger

from next_task.services import models


class LoadTemplate:
    """Load the template file."""

    def __init__(self):
        """Instansiate the class."""
        with open("next_task/services/template.json", "r") as file:
            self.data = json.load(file)
        if self.data == {}:
            logger.warning("Template file is empty\n"
                           "\tPackage template file is located in"
                           "next_task_services/")
            sys.exit()


class CheckTaskStore:
    """Confirm task file exits."""

    def __init__(self):
        """Instansiate the Check class."""
        self.file = f"{str(Path.home())}/.tasks.json"
        self.exists()

    def exists(self):
        """Check that the path exists."""
        if Path(self.file).exists():
            return True
        with open(self.file, "a+") as file:
            file.seek(0)
            json.dump(LoadTemplate().data, file, indent=4)


class GetTasks:
    """Opens up the task file and returns the json as a python dictionary."""

    def __init__(self):
        """Instansiate the class."""
        with open(CheckTaskStore().file, "r") as file:
            self.file_data = json.load(file)
        self.file_data = models.CheckFormatting(self.file_data).data


class WriteTask:
    """Write to .tasks.json."""

    def __init__(self, data: dict):
        """Instansiate the Write Class."""
        self.file = CheckTaskStore().file
        self.data = models.CheckFormatting(data).data
        logger.info(
            f"Writing {self.data['task_count']} tasks to {self.file}"
        )
        with open(self.file, "r+") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)
