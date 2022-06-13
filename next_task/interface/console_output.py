"""Format the console output."""

from rich.theme import Theme
from rich.console import Console


class Format:
    """Pre-formatted rich styled output."""

    def __init__(self):
        """Instansiate the class."""
        self.task = Theme({
            "default": "default",
            "info": "#C69400",
            "warning": "#BA2D0B",
            "highlight": "#ADD9F4",
            "number": "#ADD9F4",
            "pass": "#09814A"
        }, inherit=False)


class CreateTask:
    """Format text output for task output."""

    def __init__(self, data):
        """Instanisate the class."""
        self.id = data["id"]
        self.summary = data["summary"]
        self.due = data["due"]

    def print(self):
        """Print to the console."""
        console = Console(theme=Format().task)
        console.print(
            f"[b]Created task {self.id}: [/b]"
            f"[highlight]{self.summary}[/highlight]\n"
            f"Due: {self.due}",
            style="info"
        )
