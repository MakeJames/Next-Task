"""Service module containing methods relating to the task file."""

import sqlite3
import os


class Database:
    """Database detail."""

    _version = 0.1
    _folder = f"{os.path.expanduser('~')}/Notes/nextTask"
    _file = f"{_folder}/task.db"


class Setup(Database):
    """Establish database connection."""

    def __init__(self):
        """Instansiate the class."""
        Database.__init__(self)
        os.makedirs(self._folder, exist_ok=True)
        self.conn = sqlite3.connect(self._file)
        self.curs = self.conn.cursor()
        self.confirm_database_schema_exists()
        if self.check_database_version_is_latest():
            return
        else:
            # TODO: write update method
            print(
                f"Database running on {self.database_version}.",
                f"Current database version is {self._version}")

    def confirm_database_schema_exists(self) -> None:
        """Check that the schema exists."""
        self.curs.execute("""
            SELECT count(name) FROM sqlite_master
            WHERE type='table'
            AND name='task_database_version';
        """)
        if self.curs.fetchone()[0] == 0:
            _setup_file = os.path.join(os.path.dirname(__file__), "setup.sql")
            with open(_setup_file, "r") as file:
                self.curs.executescript(file.read())

    def check_database_version_is_latest(self):
        """Validate that the database is running the latest version."""
        self.curs.execute("""
            SELECT version FROM task_database_version
        """)
        self.database_version = self.curs.fetchone()[0]
        if self.database_version == self._version:
            return True
        return False
