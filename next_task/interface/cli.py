"""Command line script."""

import argparse
import sys

import next_task
from next_task.interface import console_output
from next_task.services import tasks


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
    parser.add_argument(
        "-d",
        "--done",
        help="""
            Mark the current task as done
        """,
        action="store_true"
    )
    parser.add_argument(
        "-l",
        "--list",
        help="""
            Lists open tasks
        """,
        action="store_true"
    )

    args = parser.parse_args(argv)

    if args.add:
        tasks.CreateTask(args.add)
    if args.task:
        tasks.GetNextTask().print()
    if args.skip:
        tasks.SkipTask()
    if args.done:
        tasks.MarkAsClosed()
    if args.list:
        console_output.ListTasks(tasks.GetNextTask().file.data)


if __name__ == "__main__":
    sys.exit(main())
