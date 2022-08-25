"""Module containing the methods relating to task creation."""

import datetime
import secrets
from datetime import datetime as dt
from datetime import timedelta
from sys import exit

from next_task.interface import console_output
from next_task.services.store import GetTasks, WriteTask


class TaskData:
    """Instansate the data in the Task file."""

    def __init__(self):
        """Map the task file to the class."""
        data = GetTasks().file_data
        for key in data:
            setattr(self, key, data[key])


class TimeStamp:
    """Return the date as a standard format."""

    date_format = "%Y-%m-%d %H:%M:%S"
    now = dt.now().strftime(date_format)
    due = (dt.now()+timedelta(days=7)).strftime(date_format)


class GetPriority:
    """Return the next priority task."""

    def __init__(self, task_data):
        """Instansiate the class."""
        self.data = task_data
        self.data["tasks"].sort(key=self.calculate)

    def calculate(self, item):
        """Compound function of the due date and created date."""
        created = dt.strptime(
            item["created"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        due = dt.strptime(
            item["due"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        call = created * (due - created) * 0.6
        return call


class CreateTask:
    """Creates a task entry."""

    def __init__(self, task_count: int, summary):
        """Instansiate the Create task class."""
        time_stamp = TimeStamp()
        self.id = task_count + 1
        self.summary = str(summary)
        self.created = time_stamp.now
        self.due = time_stamp.due


class GetNextTask:
    """Return the Next highest priority Task."""

    def __init__(self, data=None):
        """Instansiate the get task wrapper class."""
        self.get_tasks(data)
        self.file = GetPriority(self.data)
        self.get_current_task()

    def get_tasks(self, data):
        """Check if data is supplied and if if not get task data."""
        self.file_data = GetTasks().file_data
        if data is None:
            self.data = self.file_data
            return
        self.data = data

    def check_tasks(self):
        """Handle the error of no tasks."""
        if self.file.data["tasks"] == []:
            console_output.Congratulations()
            WriteTask(self.file_data)
            exit([0])

    def get_current_task(self):
        """Return the current or next task."""
        self.check_tasks()
        if "current" not in self.file.data:
            self.next_task = self.file.data["tasks"][0]
            self.file_data["current"]["task"] = self.next_task
            return

        if "id" not in self.file.data["current"]["task"]:
            self.next_task = self.file.data["tasks"][0]
            self.file_data["current"]["task"] = self.next_task
            return

        self.next_task = self.file_data["current"]["task"]

    def print_task(self):
        """Print the next task."""
        console_output.Format(self.next_task).next_task()
        WriteTask(self.file_data)


class SkipTask:
    """Skip the next highest priority task."""

    def __init__(self, data=None):
        """Instansiate the class."""
        self.tasks = GetNextTask(data)
        console_output.Format(self.tasks.next_task).skip_task()
        self.update_file_data()
        GetNextTask(self.tasks.file.data).print_task()

    def update_due_date(self):
        """Update Task due date."""
        date = dt.strptime(
            self.tasks.next_task["due"],
            "%Y-%m-%d %H:%M:%S"
        )
        add_days = secrets.randbelow(8)
        new_date = date + datetime.timedelta(days=add_days)
        self.tasks.next_task["due"] = new_date.strftime("%Y-%m-%d %H:%M:%S")

    def update_file_data(self):
        """Find task and update due date."""
        tasks = self.tasks.file.data["tasks"]
        if "current" in self.tasks.file.data:
            self.tasks.file.data["current"]["task"] = {}
        for index in range(len(tasks)):
            if tasks[index]["id"] == self.tasks.next_task["id"]:
                self.update_due_date()
                tasks[index] = self.tasks.next_task
                break


class MarkAsClosed:
    """Mark a task as closed."""

    def __init__(self, data=None):
        """Instansiate the class."""
        self.tasks = GetNextTask(data)
        self.update()
        console_output.Format(self.tasks.next_task).mark_closed()
        GetNextTask(self.tasks.file.data).print_task()

    def update(self):
        """Update the task."""
        self.tasks.file.data["tasks"].remove(self.tasks.next_task)
        self.tasks.next_task["status"] = "closed"
        now = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tasks.next_task["completed"] = now
        self.tasks.file.data["completed"]["tasks"].append(self.tasks.next_task)
        if "current" in self.tasks.file.data:
            self.tasks.file.data["current"]["task"] = {}
