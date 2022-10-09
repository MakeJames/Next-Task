"""Main application of Next Task."""

from .interface import cli
from .interface.console_output import Style
from .services import tasks, projects, database

console = Style().console()


def operation(chosen_operation, _args=None):
    """Map user args to app targets."""
    if _args[0] is True:
        _args = []

    ops = {
        "project": projects.SetActive,
        "add-project": projects.CreateProject,
        "clear": projects.ClearActive,
        # "complete project":
        "add": tasks.CreateTask,
        "task": tasks.GetNextTask().print,
        "skip": tasks.SkipTask,
        "done": tasks.CloseTask
    }

    chosen_operation_function = ops.get(chosen_operation)

    return chosen_operation_function(*_args)


def main():
    """Command Line function of Next Task."""
    database.CheckDatabase()
    console.print("-" * 50)
    projects.CheckActiveProject().print()
    action = 0
    for key, value in vars(cli.parse_args()).items():
        if value:
            operation(key, [value])
            action += 1

    if action == 0:
        tasks.ListTasks()
    console.print("-" * 50)
