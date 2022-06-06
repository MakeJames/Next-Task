"""Service module containing methods relating to the task file."""

import json
import sys
from pathlib import Path

from loguru import logger


class LoadTemplate:
    """Load the template file."""

    def __init__(self):
        """Instansiate the class."""
        with open("next_task/services/template.json", "r") as file:
            self.data = json.load(file)
        if self.data == {}:
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
            logger.debug(f"{self.file} does not exist, creating file")
            # TODO: Move to a template write class
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
            self.file_data = json.load(file)


class WriteTask:
    """Write to .tasks.json."""

    def __init__(self, data: dict):
        """Instansiate the Write Class."""
        self.file = Check().file
        self.data = data
        self.validate_data_input()
        logger.debug(
            f"Writing {len(self.data['tasks'])} tasks to {self.file}"
        )
        with open(self.file, "r+") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)

    def validate_data_input(self):
        """Provide defensive steps to guard against deletion of task data."""
        if self.data == {}:
            logger.warning(
                "Task data is empty, this opperation will ",
                "override all data in .tasks.json"
            )
            # TODO: call template function
            raise AttributeError("Task data is empty.")
        if self.data["tasks"] == []:
            logger.warning(
                "This oppoeration will overide all data in .tasks.json"
            )
            # TODO: call an 'are you sure' function
            raise AttributeError("Task data is empty.")
