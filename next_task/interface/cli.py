"""Command line script."""

import argparse
import os
import sys

import next_task
from next_task.services import store, tasks


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
    parser.add_argument(
        "-a",
        "--add",
        help="""
            Create a task in the format --add 'Your Task name'.
            Adds one task at a time.
        """,
        type=str
    )
    parser.add_argument(
        "-t",
        "--task",
        help="""
            Returns the next task to be done
        """,
        action="store_true"
    )
    parser.add_argument(
        "-s",
        "--skip",
        help="""
            Skips the current top task.
        """,
        action="store_true"
    )

    args = parser.parse_args(argv)

    if args.check_file:
        store.Check()
        sys.exit()
    if args.add:
        tasks.CreateTask(args.add)
        sys.exit()
    if args.task:
        tasks.GetNextTask().print_task()
        sys.exit()
    if args.skip:
        tasks.SkipTask()
        sys.exit()


if __name__ == "__main__":
    sys.exit(main())
