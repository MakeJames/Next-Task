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
            "warning": "#C92727",
            "highlight": "#ADD9F4",
            "number": "#ADD9F4",
            "pass": "#4A70C2"

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


class NextTask:
    """Format console output for returning the next task."""

    def __init__(self, data):
        """Instanisate the class."""
        self.id = data["id"]
        self.summary = data["summary"]
        self.due = data["due"]

    def print(self):
        """Print to the console."""
        console = Console(theme=Format().task)
        console.print(
            f"[b][#5CE521]{self.id}:[/#5CE521] {self.summary}[/b]\n"
            f"[warning]Due:[/warning] [default]{self.due}[/default]",
            style="pass"
        )


class SkipTask:
    """Format console output when skiping the next task."""

    def __init__(self, data):
        """Instanisate the class."""
        self.id = data["id"]
        self.summary = data["summary"]
        self.due = data["due"]

    def print(self):
        """Print to the console."""
        console = Console(theme=Format().task)
        console.print(
            f"[warning]updated {self.id}:[/warning] {self.summary}\n"
            f"[info]now due: {self.due}[/info]",
            style="pass"
        )
