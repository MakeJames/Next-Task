"""Module containing the methods relating to task creation."""

import datetime
import json
import random
import sys

from loguru import logger

from next_task.services import store


class GetPriority:
    """Return the next priority task."""

    def __init__(self, task_data):
        """Instansiate the class."""
        logger.info("calculating task list priority")
        self.data = task_data
        self.data["tasks"].sort(key=self.calculate)

    def calculate(self, item):
        """Compound function of the due date and created date."""
        # TODO: priority should be inherited from project
        created = datetime.datetime.strptime(
            item["created"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        due = datetime.datetime.strptime(
            item["due"],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        call = created * (due - created) * 0.6
        return call


class CreateTask:
    """Setup class to create the structure of the json file."""

    def __init__(self, summary: str):
        """Instansiate the Write task class."""
        self.summary = summary
        self.file_data = store.GetTasks().file_data
        self.task_formatter()
        store.WriteTask(self.file_data)
        print(f"Created task {self.id}: {self.summary}\n"
              f"Due: {self.due.strftime('%Y-%m-%d %H:%M:%S')}")

    def task_formatter(self):
        """Build task dictionary."""
        self.id = self.file_data["task_count"] + 1
        logger.info(f"formating task {self.id}")
        self.file_data["task_count"] = self.id
        now = datetime.datetime.now()
        self.due = now + datetime.timedelta(days=7)
        task = {
            "id": self.id,
            "summary": self.summary,
            "created": now.strftime("%Y-%m-%d %H:%M:%S"),
            "due": self.due.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "open"
        }
        logger.info(f"Creating task {task['id']}: "
                    f"{task['summary']}"
                    f" - {task['created']}")
        self.file_data["tasks"].append(task)


class GetNextTask:
    """Print the next task to the command line."""

    def __init__(self):
        """Instansiate the get task wrapper class."""
        self.file_data = store.GetTasks().file_data
        self.ordered_tasks = GetPriority(self.file_data).data
        self.get_task()

    def get_task(self):
        """Get the next task, handles the error of no tasks."""
        try:
            self.task = self.ordered_tasks["tasks"][0]
            logger.info(f"next priority task is {self.task['id']}")
        except IndexError:
            logger.debug("list index 0 out of range")
            print("Congratulations!\n"
                  "There are no tasks on your to do list\n"
                  "Take a break and have a cup of tea.")
            sys.exit()

    def print_task(self):
        """Print the next task."""
        print(f"{self.task['id']}: {self.task['summary']}\n"
              f"due {self.task['due']}")


class SkipTask:
    """Skip the next task."""

    def __init__(self):
        """Instansiate the class."""
        self.all_tasks = GetNextTask()
        self.task = self.all_tasks.task
        self.update_file_data()
        store.WriteTask(self.all_tasks.file_data)
        GetNextTask().print_task()

    def update_due_date(self):
        """Update Task due date."""
        self.date = datetime.datetime.strptime(
            self.task["due"],
            "%Y-%m-%d %H:%M:%S"
        )
        add_days = random.uniform(0.5, 8)
        logger.info(f"Increase by {add_days}")
        self.new_date = self.date + datetime.timedelta(days=add_days)
        logger.info(f"Updating due date from {self.task['due']}, "
                    f"now due {self.new_date}")
        self.task["due"] = self.new_date.strftime("%Y-%m-%d %H:%M:%S")

    def update_file_data(self):
        """Find task and update due date."""
        tasks = self.all_tasks.file_data["tasks"]
        logger.debug('updating file_data')
        for index in range(len(tasks)):
            logger.debug(f"checking {tasks[index]['id']}")
            if tasks[index]["id"] == self.task["id"]:
                self.update_due_date()
                tasks[index] = self.task
                print(f"updated {tasks[index]['id']}: "
                      f"{tasks[index]['summary']}\n"
                      f"now due: {tasks[index]['due']}")
                break


class MarkAsClosed:
    """Mark a task as closed."""

    def __init__(self):
        """Instansiate the class."""
        self.get_tasks = GetNextTask()
        self.task = self.get_tasks.task
        self.file_data = self.get_tasks.file_data
        self.file_data["tasks"].remove(self.task)
        logger.debug(f"removed {self.task['id']} from task data")
        self.update()
        logger.debug(f"adding {self.task['id']} to completed tasks")
        self.file_data["completed_tasks"].append(self.task)
        store.WriteTask(self.file_data)

    def update(self):
        """Update the task."""
        self.task["status"] = "closed"
        now = datetime.datetime.now()
        self.task["completed"] = now.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Updating {self.task['id']}: {self.task['summary']}'")
        print(f"updated {self.task['id']}, ",
              f"completed: {self.task['completed']}")
