"""Command line script."""

import argparse
import sys

import next_task


def main(argv=None):
    """Provide options for the package."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-v",
        "--version",
        help="show current version",
        action="version",
        version=f"Next: {next_task.__version__}"
    )
    parser.add_argument(
        "-p",
        "--project",
        help="""
            Targest a given project
        """,
        nargs="?",
        const=True
    )
    group.add_argument(
        "-a",
        "--add",
        help="""
            Create a task in the format --add 'Your Task name'.
            Adds one task at a time.
        """,
        type=str
    )
    group.add_argument(
        "-t",
        "--task",
        help="""
            Returns the next task to be done
        """,
        action="store_true"
    )
    group.add_argument(
        "-d",
        "--done",
        help="""
            Mark the current task as done
        """,
        action="store_true"
    )
    group.add_argument(
        "-s",
        "--skip",
        help="""
            Skips the current top task.
        """,
        action="store_true"
    )
    group.add_argument(
        "-c",
        "--clear",
        help="""
            Clear the current project and return
            to the normal task list
        """,
        action="store_true"
    )

    args = parser.parse_args(argv)

    # 1. set project / return current project
    # one of:
    # add -- just add task
    # task
    # done
    # skip
    # clear
    print(vars(args))

    sys.exit()
