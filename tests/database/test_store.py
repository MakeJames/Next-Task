"""Module to test the methods of the store Module."""

import sqlite3
import os

import pytest
from pytest_mock import mocker

from next_task.database import store


class TestDatabaseClass:
    """Test the methods of the Database Class."""

    def test_database_target_is_as_expected(self, mock_sqlite, tmpdir) -> None:
        """R-BICEP: Right."""
        expected_database = f"{tmpdir}/Notes/nextTask/task.db"
        database = store.Database()
        assert expected_database == database.database_path

    def test_set_up_file_is_targetting_a_file(self, mock_sqlite) -> None:
        """R-BICEP: Right."""
        expected_setup_file = str(
            os.path.dirname(__file__)
        ).replace(
            "tests/database",
            "next_task/database/setup.sql"
        )
        database = store.Database()
        assert expected_setup_file == database._setup_file

    def test_database_version_attribute_is_same_as_setup_file(self) -> None:
        """R-BICEP: Right."""
        database = store.Database()
        assert database._version == database.database_version
