"""Command line script."""

import argparse

import next_task


def parse_args(argv=None):
    """Provide options for the package."""
    parser = argparse.ArgumentParser(
        description="""Next Task is a task management solution for those that
want to avoid the faff.

Task mnanagement is a mundane feature of life with paper form task
lists being superior to must task management solutions for simplicity.
Many graphically focused task management solutions focus on the design
of the task or custom workflow rather than focusing on getting the task
done.

This application focuses on serving a user with a task to either progress
or skip.

Tasks are a discrete unit of work that can be actioned in isolation.
They should be identifable and specific so that you can
Some tasks might read as
\t- "email Frank the notes from yesterday's meeting"
\t- "Review the latest quarterly notes"
        """,
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-v",
        "--version",
        help="show current version",
        action="version",
        version=f"Next: {next_task.__version__}"
    )
    group.add_argument(
        "-p",
        "--project",
        help="""Set a project as active as [Next -p 'Project Name']. Projects
remain active until cleared (with -c), or a new project is selected.
To view the current active project use [Next -p].

If the project doesn't exist, or the user enters the wrong name,
the user will be prompted to create the project or select from a
currently existing project.

All task related actions will be performed within the project
eg:
\t Next -a "A new task" creates a new task in the project.
        """,
        nargs="?",
        const=True
    )
    group.add_argument(
        "-ap",
        "--add-project",
        help="Create a project [Next --add_project 'Project Name'",
        type=str
    )
    group.add_argument(
        "-a",
        "--add",
        help="Create a task [Next --add 'Your Task name']",
        type=str
    )
    group.add_argument(
        "-t",
        "--task",
        help="Returns the next task to be done",
        action="store_true"
    )
    group.add_argument(
        "-d",
        "--done",
        help="Mark the current task as done",
        action="store_true"
    )
    group.add_argument(
        "-s",
        "--skip",
        help="Skips the current top task.",
        action="store_true"
    )
    group.add_argument(
        "-c",
        "--clear",
        help="Clear the current project to return to the global task list",
        action="store_true"
    )

    return parser.parse_args(argv)
