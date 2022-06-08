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


class Check:
    """Confirm task file exits."""

    def __init__(self):
        """Instansiate the Check class."""
        self.file = self._file_path_builder()
        self.exists()

    def _file_path_builder(self):
        home = str(Path.home())
        return f"{home}/.tasks.json"

    def exists(self):
        """Check that the path exists."""
        if not Path(self.file).exists():
            logger.info(f"{self.file} does not exist, creating file")
            with open(self.file, "a+") as file:
                file.seek(0)
                json.dump(LoadTemplate().data, file, indent=4)
            print("created .tasks.json")
        else:
            logger.debug(f"Task file path exists: {self.file}")


class GetTasks:
    """Opens up the task file and returns the json as a python dictionary."""

    def __init__(self):
        """Instansiate the class."""
        with open(Check().file, "r") as file:
            logger.info("fetching file data")
            self.file_data = json.load(file)
        self.file_data = models.CheckFormatting(self.file_data).data


class WriteTask:
    """Write to .tasks.json."""

    def __init__(self, data: dict):
        """Instansiate the Write Class."""
        self.file = Check().file
        self.data = models.CheckFormatting(data).data
        logger.info(
            f"Writing {self.data['task_count']} tasks to {self.file}"
        )
        with open(self.file, "r+") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)
