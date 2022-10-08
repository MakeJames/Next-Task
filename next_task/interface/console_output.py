"""Format the console output."""

from rich import box
from rich.console import Console
from rich.table import Table
from rich.theme import Theme


class Style:
    """Hold the Theme definitions for the package."""

    task_theme = Theme(
        {
            "default": "default",
            "info": "#C69400",
            "warning": "#C92727",
            "highlight": "#ADD9F4",
            "green": "#09814A"
        },
        inherit=True
    )

    def console(self):
        """Instnasiate the Console Class."""
        return Console(theme=self.task_theme)


class TaskTable:
    """Returns a formatted table of tasks to the command line."""

    def __init__(self, data: list, title="Open Tasks"):
        """Insttansiate the class."""
        if data is None:
            return
        table = Table(title=title)
        table.box = box.SIMPLE_HEAD
        table.add_column("Id", style="#C69400", no_wrap=True)
        table.add_column("Summary", style="#ADD9F4", no_wrap=True)
        for row in data:
            table.add_row(
                f"{row[0]}",
                f"{row[1]}",
            )
        Console().print(table, justify="left")
