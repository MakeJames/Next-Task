"""Module containing the methods relating to task creation."""

import secrets
from datetime import datetime as dt
from datetime import timedelta
from next_task.interface import console_output
from next_task.services.store import GetTasks, WriteTask


class TaskData:
    """Instansate the data in the Task file."""

    def __init__(self):
        """Map the task file to class variables."""
        data = GetTasks().file_data
        for key in data:
            setattr(self, key, data[key])


class TimeStamp:
    """Return the date as a standard format."""

    _date_format = "%Y-%m-%d %H:%M:%S"
    _short_format = "%Y-%m-%d"
    now = dt.now().strftime(_date_format)
    due = (dt.now()+timedelta(days=7)).strftime(_date_format)

    def convert_from_string(self, date_time):
        """Unpack string of time."""
        if isinstance(date_time, dt):
            return date_time
        return dt.strptime(date_time, self._date_format)

    def convert_to_string(self, date_time):
        """Format datetime object of time."""
        if isinstance(date_time, str):
            return date_time
        return date_time.strftime(self._date_format)

    def short(self, time):
        """Format date as Year-month-day."""
        date_time = self.convert_from_string(time)
        return date_time.strftime(self._short_format)


class CreateTask:
    """Creates a task entry."""

    def __init__(self, task_count: int, summary):
        """Instansiate the Create task class."""
        time_stamp = TimeStamp()
        self.id = task_count + 1
        self.summary = str(summary)
        self.created = time_stamp.now
        self.due = time_stamp.due
        self.skip_count = 0


class GetNextTask:
    """Return the Next highest priority Task."""

    # TODO: Think of a way to handle project tasks.
    # ???: This class is still donig too much
    # ???: -- this function should simply set next task, not
    # ???: -- wrap the TaskData class.

    def __init__(self, data=None):
        """Instansiate the get next task class."""
        self._check_data(data)
        if self.task_data.current["project"]:
            # TODO: if project data then...
            # Check current task in project
            # if True, return current task
            # if False get current project task
            pass
        if self.task_data.current["task"]:
            return
        if self.task_data.tasks:
            self.task_data.tasks.sort(key=self.get_priority)
            self.task_data.current["task"] = self.task_data.tasks[0]
            return
        console_output.Congratulations()

    def _check_data(self, data):
        if data:
            self.task_data = data
            return
        self.task_data = TaskData()

    def get_priority(self, item):
        """Return the next priority task."""
        created = TimeStamp().convert_from_string(item["created"]).timestamp()
        due = TimeStamp().convert_from_string(item["due"]).timestamp()
        if "skip_count" in item:
            rand_num = secrets.SystemRandom().uniform(0.001, 1.0)
            return created + ((due * item["skip_count"]) / rand_num)
        item["skip_count"] = 0
        return created

    # TODO: Method outside of scope for class - move
    def print_task(self):
        """Print the next task."""
        if self.task_data.current["task"]:
            console_output.Format(self.task_data.current["task"]).next_task()
        WriteTask(self.task_data.__dict__)


class SkipTask:
    """Skip the next highest priority task."""

    def __init__(self, data):
        """Instansiate the class."""
        # TODO: should accept data input rather than call Next Task
        self.task_data = data
        task = self.task_data.current["task"]
        self.task_data.current["task"] = {}
        for index in range(len(self.task_data.tasks)):
            if self.task_data.tasks[index]["id"] == task["id"]:
                self.task_data.tasks[index]["skip_count"] += 1
                self.skip_task = self.task_data.tasks[index]
                break


class MarkAsClosed:
    """Mark a task as closed."""

    def __init__(self, data):
        """Instansiate the class."""
        # TODO: should accept data input rather than call Next Task
        self.task_data = data
        self.task_data.tasks.remove(self.task_data.current["task"])
        self.task_data.current["task"]["status"] = "closed"
        self.task_data.current["task"]["completed"] = TimeStamp().now
        self.task_data.completed["tasks"].append(
            self.task_data.current["task"]
        )
        self.closed_task = self.task_data.current["task"]
        self.task_data.current["task"] = {}
