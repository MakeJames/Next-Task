"""Command line script."""

import argparse
import os
import sys

import next_task
from next_task.services import file


def main(argv=None):
    """Provide options for the package."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        help="show current version",
        action="version",
        version=f"Next: {next_task.__version__}"
    )
    parser.add_argument(
        "--check-file",
        help="""
            Validate that the task file exists, if not
            creates an empty task file in the home directory.
        """,
        action="store_true"
    )

    args = parser.parse_args(argv)

    if args.check_file:
        check = file.Check()
        sys.exit()


if __name__ == "__main__":
    sys.exit(main())
