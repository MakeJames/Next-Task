"""Module to test the methods of the store Module."""

import sqlite3
import os

import pytest
from pytest_mock import mocker

from next_task.database import store


class TestSetupClass:
    """Test the methods of the Database Class."""

    def test_database_version_attribute_is_same_as_setup_file(
        self,
        test_db
    ) -> None:
        """R-BICEP: Right."""
        assert store.Setup().create_database() == store.version
