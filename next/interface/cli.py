"""Command line script."""

import argparse
import os
import sys

import next


def main(argv=None):
    """Provide options for the package."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        help="show current version",
        action="version",
        version=f"Next: {next.__version__}"
    )

    args = parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
