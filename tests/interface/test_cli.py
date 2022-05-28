"""Test the methods of the cli module."""

import pytest

from next.interface import cli
from next import __version__


class TestCliMainMethod:
    """Test the main method of the cli module."""

    def test_main_version(
        self,
        capsys
    ) -> None:
        """R-BICEP: Right."""
        with pytest.raises(SystemExit):
            cli.main(["--version"])
        captured = capsys.readouterr()
        assert captured.out == f"Next: {__version__}"
