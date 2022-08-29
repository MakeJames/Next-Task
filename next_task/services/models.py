"""Model the various data structures of the project."""

from datetime import timedelta


class Constructor:
    """Data class for current Tasks."""

    def __init__(self, **kwargs):
        """Unpack the class kwargs."""
        self.field = {}
        for key, value in kwargs.items():
            self.field[key] = value


class Task:
    """Data class for a task."""

    def __init__(self, id, summary, now):
        """Instansiate the Task model."""
        self.id = id
        self.summary = str(summary)
        self.created = now.strftime("%Y-%m-%d %H:%M:%S")
        self.due = (now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")


class Project:
    """Data class for a project."""

    def __init__(self, id, summary, now):
        """Instansiate the Project model."""
        self.id = str(id)
        self.summary = str(summary)
        self.created = now
        self.task_count = 0
        self.tasks = []
        self.completed = {"tasks": []}


class TemplateTaskFile:
    """Data class for the task file."""

    def __init__(self):
        """Instansiate the Task file class."""
        self.current = Constructor(task={}, project={}).field
        self.tasks = []
        self.task_count = 0
        self.completed = Constructor(tasks=[], projects=[]).field
        self.projects = []
