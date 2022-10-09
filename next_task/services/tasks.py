"""Module containing the methods relating to task creation."""

from pypika import Query, Table
from rich.markup import escape

from next_task.interface.console_output import Style, TaskTable

from .database import Database

console = Style().console()


class CreateTask:
    """Create a task."""

    def __init__(self, task_summary):
        """Instansiate the class."""
        task = Table('task')
        query = Query.into(task).columns('summary')
        new_task = Database().write(str(query.insert(task_summary)))
        console.print(f"[info][b]Created Task {new_task}:[/b][/info]",
                      f"[highlight]{escape(task_summary)}[/highlight]")


class GetNextTask:
    """Return the next task in the task db."""

    def __init__(self):
        """Instansiate the class."""
        query = "SELECT task_id, summary FROM task_list LIMIT 1;"
        self.task = Database().read(str(query))

    def print(self):
        """Print the task to the console."""
        if self.confirm_next_task():
            id = self.task[0]['task_id']
            summary = self.task[0]['summary']
            console.print(f"[info][b]{id}: [/b][/info]{escape(summary)}",
                          style="highlight")
        else:
            console.print("[green][b]Congratulations![/b] "
                          "There are no more tasks on your task list\n"
                          "Take a break and have a cup of tea.[/green]")

    def confirm_next_task(self):
        """Confirm that there is a task."""
        if self.task:
            return True
        return False


class SkipTask:
    """Skip the next task."""

    def __init__(self):
        """Instansiate the class."""
        task_skips = Table("task_skips")
        query = Query.into(task_skips).columns("task_id")
        task = GetNextTask()
        if task.confirm_next_task():
            id = task.task[0]['task_id']
            Database().write(str(query.insert(id)))
            console.print(f"[info][i]Skipped Task {id}[/i][/info]")
            GetNextTask().print()
            return
        task.print()


class CloseTask:
    """Close a task."""

    def __init__(self):
        """Instansiate the class."""
        task_status = Table('task_status')
        query = Query.into(task_status).columns("task_id", "t_status")
        task = GetNextTask()
        if task.confirm_next_task():
            task_id = task.task[0]['task_id']
            task_summary = task.task[0]['summary']
            Database().write(str(query.insert(task_id, "closed")))
            console.print(f"[green]Closed {task_id}: {task_summary}[/green]")
            GetNextTask().print()
            return
        task.print()


class ListTasks:
    """List the open tasks."""

    def __init__(self):
        """Instansiate the class."""
        self.data = Database().read("SELECT * FROM task_list;")
        TaskTable(self.data)
