"""Service module containing methods relating to the task file."""

import json
from pathlib import Path

from loguru import logger


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
                json.dump(
                    {"tasks": []},
                    file,
                    indent=4
                )
            print("created .tasks.json")
        else:
            logger.debug(f"Task file path exists: {self.file}")
