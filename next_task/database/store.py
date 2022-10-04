"""Service module containing methods relating to the task file."""

import sqlite3
import os
import sys


version = 0.4
folder = f"{os.path.expanduser('~')}/Notes/nextTask"


class Database:
    """Database detail."""

    def __init__(self, database=f"{folder}/task.db"):
        """Instansiate the class."""
        self._file = f"{database}"
        self.conn = None
        self.curs = None

    def __enter__(self):
        """Establish Database connection."""
        self.conn = sqlite3.connect(self._file)
        self.curs = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Gracefully exit the db connection."""
        if exc_val:
            print(exc_val)
            self.conn.close()
            sys.exit(exc_val)
        else:
            self.conn.commit()
            print(self.conn.total_changes)
            self.conn.close()


class CheckDatabase:
    """Establish database connection."""

    def __init__(self):
        """Instansiate the class."""
        os.makedirs(folder, exist_ok=True)
        if self.database_schema_exists() == 0:
            Setup().create_database()
            return
        if version != self.database_version_is_latest():
            os.remove(f"{folder}/task.db")
            Setup().create_database()
            return

    def database_schema_exists(self) -> None:
        """Check that the schema exists."""
        with Database() as conn:
            conn.curs.execute("""
                SELECT count(name)
                FROM sqlite_master
                WHERE name='task_database_version';
            """)
            return conn.curs.fetchone()[0]

    def database_version_is_latest(self):
        """Validate that the database is running the latest version."""
        with Database() as conn:
            conn.curs.execute("SELECT db_version FROM task_database_version")
            return conn.curs.fetchone()[0]


class Setup:
    """Setup methods to instansiate and update the database."""

    _setup = os.path.join(os.path.dirname(__file__), "setup.sql")

    def create_database(self):
        """Create the database from sql setup file."""
        with Database() as conn, open(self._setup, "r") as file:
            conn.curs.executescript(file.read())
            conn.curs.execute("SELECT db_version FROM task_database_version")
            return conn.curs.fetchone()[0]
