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
        console = Style().console()
        if data == []:
            if title != "Open Tasks":
                return
            console.print("There are no Tasks", style="green")
            return
        table = Table(title=title, title_justify="left",
                      row_styles=["highlight", ""])
        table.box = box.SIMPLE_HEAD
        table.add_column("Id", no_wrap=True)
        table.add_column("Summary", no_wrap=True)
        for row in data:
            table.add_row(
                f"{row[0]}",
                f"{row[1]}",
            )
        console.line()
        console.print(table, justify="left")
