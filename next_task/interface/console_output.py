"""Format the console output."""

from rich import box
from rich.console import Console
from rich.table import Table
from rich.theme import Theme


class Style:
    """Hold the Theme definitions for the package."""

    def __init__(self):
        """Instansiate the class."""
        task_theme = Theme({
                "default": "default",
                "info": "#C69400",
                "warning": "#C92727",
                "highlight": "#ADD9F4",
                "number": "#ADD9F4",
                "pass": "#4A70C2",
                "green": "#09814A"
            }, inherit=False)
        self.console = Console(theme=task_theme)


class ListTasks:
    """Returns a formatted table of tasks to the command line."""

    def __init__(self, data, title="Open Tasks"):
        """Insttansiate the class."""
        table = Table(title=title)

        table.box = box.SIMPLE_HEAD

        table.add_column("id", style="#09814A", no_wrap=True)
        table.add_column("summary", style="#4A70C2", no_wrap=True)
        table.add_column("created", justify="right", style="#4A70C2")

        for row in data:
            table.add_row(
                f"{row['id']}",
                f"{row['summary']}",
                f"{row['created']}"
            )

        Console().print(table, justify="left")


class Format:
    """Pre-formatted rich styled output."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        self.id = data["id"]
        self.summary = data["summary"]
        self.due = data["due"]

    def create_task(self):
        """Format text output for create task output."""
        Style().console.print(
            f"[b]Created task {self.id}: [/b]"
            f"[highlight]{self.summary}[/highlight]\n"
            f"Due: {self.due}",
            style="info"
        )

    def next_task(self):
        """Format console output for returning the next task."""
        Style().console.print(
            f"[b][#5CE521]{self.id}:[/#5CE521] {self.summary}[/b]\n"
            f"[warning]Due:[/warning] [default]{self.due}[/default]",
            style="pass"
        )

    def skip_task(self):
        """Format console output when skiping the next task."""
        Style().console.print(
            f"[warning]updated {self.id}:[/warning] {self.summary}\n"
            f"[info]now skiped: {self.data['skip_count']}[/info]",
            style="pass"
        )

    def mark_closed(self):
        """Format console output for closing a task."""
        Style().console.print(
            f"[b]Updated {self.id},[/b] "
            f"Completed: [default]{self.data['completed']}[/default]",
            style="green"
        )


class Congratulations:
    """Format console output when there are no more tasks to do."""

    def __init__(self):
        """Instansiate the class."""
        Style().console.print(
            "[b]Congratulations![/b]\n"
            "There are no tasks on your to do list\n"
            "Take a break and have a cup of tea.",
            style="green"
        )


class FormatProject:
    """Format the output for projects."""

    def __init__(self, data):
        """Instansiate the class."""
        self.data = data
        self.id = data["id"]
        self.summary = data["summary"]

    def create(self):
        """Format text output for create task output."""
        Style().console.print(
            f"[b]Created project {self.id}: [/b]"
            f"[highlight]{self.summary}[/highlight]",
            style="info"
        )
