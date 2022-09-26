"""Module to test the methods of the store Module."""

import sqlite3
import os

import pytest
from pytest_mock import mocker

from next_task.database import store


class TestSetupClass:
    """Test the methods of the Database Class."""

    def test_database_target_is_as_expected(self, mock_sqlite, tmpdir) -> None:
        """R-BICEP: Right."""
        expected_database = f"{tmpdir}/Notes/nextTask/task.db"
        database = store.Setup()
        assert expected_database == database._file

    def test_database_version_attribute_is_same_as_setup_file(self) -> None:
        """R-BICEP: Right."""
        database = store.Setup()
        assert database._version == database.database_version
