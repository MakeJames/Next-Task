"""Service module containing methods relating to the task file."""

import sqlite3
import os


class Database:
    """Database detail."""

    _version = 0.2
    _folder = f"{os.path.expanduser('~')}/Notes/nextTask"
    _file = f"{_folder}/task.db"

    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self._file)
        self.curs = self.conn.cursor()


class Setup(Database):
    """Establish database connection."""

    def __init__(self):
        """Instansiate the class."""
        Database.__init__(self)
        os.makedirs(self._folder, exist_ok=True)
        self.connect()
        self.curs = self.conn.cursor()
        Check().database_schema_exists(self.curs)
        Check().database_version_is_latest(self.curs, self._version)


class Check:
    """Check functions to make sure Database is valid."""

    def database_schema_exists(self, curs) -> None:
        """Check that the schema exists."""
        curs.execute("""
            SELECT count(name) FROM sqlite_master
            WHERE type='table'
            AND name='task_database_version';
        """)
        if curs.fetchone()[0] == 0:
            _setup_file = os.path.join(os.path.dirname(__file__), "setup.sql")
            with open(_setup_file, "r") as file:
                curs.executescript(file.read())

    def database_version_is_latest(self, curs, version):
        """Validate that the database is running the latest version."""
        curs.execute("SELECT version FROM task_database_version")
        self.database_version = curs.fetchone()[0]
        if self.database_version == version:
            return
        print(f"Database running on {self.database_version}.",
              f"Current database version is {version}")
        return
