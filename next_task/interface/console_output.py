"""Format the console output."""

from rich.console import Console
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
            f"[info]now due: {self.due}[/info]",
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
