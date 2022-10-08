"""Module to test the methods of the store Module."""

import sqlite3
import os

import pytest
from pytest_mock import mocker

from next_task.services import database


class TestSetupClass:
    """Test the methods of the Database Class."""

    @pytest.mark.integration
    def test_mock_database_is_instansiated(
        self,
        mock_database
    ) -> None:
        """R-BICEP: Right."""
        expected = 0
        database.Setup().create_database()
        with database.Connection() as conn:
            conn.curs.execute("Select COUNT(*) FROM task;")
            task_count = conn.curs.fetchone()[0]
        assert task_count == expected
