"""Service module containing methods relating to the task file."""

import json
from pathlib import Path

from loguru import logger


class Check:
    """Confirm task file exits."""

    def __init__(self):
        """Instansiate the Check class."""
        self.home = str(Path.home())
        logger.debug(f"Home directory: {self.home}")
        self.file = f"{self.home}/.tasks.json"
        self.exists()

    def exists(self):
        """Check that the path exists."""
        if not Path(self.file).exists():
            logger.debug(f"{self.file} does not exist, creating file")
            file = open(self.file, "a")
            file.close()
            print("created .tasks.json")
        else:
            logger.debug(f"{self.file} exists")
