"""Service module containing methods relating to the task file."""

import sqlite3
import os

version = 0.5
folder = f"{os.path.expanduser('~')}/Notes/nextTask"


class Connection:
    """Database connection context manager."""

    def __init__(self):
        """Instansiate the class."""
        self._file = f"{folder}/task.db"
        self.conn = None
        self.curs = None

    def __enter__(self):
        """Establish Database connection."""
        self.conn = sqlite3.connect(self._file)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Gracefully exit the db connection."""
        if exc_val:
            self.conn.close()
            return False
        else:
            self.conn.commit()
            self.conn.close()


class Database:
    """Manage the connections to the database."""

    def write(self, sql):
        """Write information to the database."""
        with Connection() as conn:
            conn.curs.execute(sql)
            lastrowid = conn.curs.lastrowid
        return lastrowid

    def read(self, sql):
        """Read and return information from the database."""
        with Connection() as conn:
            conn.curs.execute(sql)
            result = conn.curs.fetchall()
        return result


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
        with Connection() as conn:
            conn.curs.execute("""
                SELECT count(name)
                FROM sqlite_master
                WHERE name='task_database_version';
            """)
            return conn.curs.fetchone()[0]

    def database_version_is_latest(self):
        """Validate that the database is running the latest version."""
        select_db_version = "SELECT db_version FROM task_database_version"
        with Connection() as conn:
            conn.curs.execute(select_db_version)
            return conn.curs.fetchone()[0]


class Setup:
    """Setup methods to instansiate and update the database."""

    _setup = os.path.join(os.path.dirname(__file__), "setup.sql")

    def create_database(self):
        """Create the database from sql setup file."""
        db_version = """
            INSERT INTO task_database_version
                (db_version)
            VALUES
                (?)
        """
        select_db_version = "SELECT db_version FROM task_database_version"

        with Connection() as conn, open(self._setup, "r") as file:
            conn.curs.executescript(file.read())
            conn.curs.execute(db_version, [version])
            conn.curs.execute(select_db_version)
            return conn.curs.fetchone()[0]
