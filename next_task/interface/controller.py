"""Manage the methods of the cli arguments."""

from next_task.interface.console_output import Format, ListTasks
from next_task.services.projects import (CloseNextTaskInProject, CreateProject,
                                         CreateProjectTask, FindProject,
                                         GetNextTaskFromProject,
                                         SkipNextTaskInProject)
from next_task.services.store import GetTasks, WriteTask
from next_task.services.tasks import (CreateTask, GetNextTask, MarkAsClosed,
                                      SkipTask, TaskData)


class Arguments:
    """Unpack the arguments entered in the cli."""

    def __init__(self, project, **kwargs):
        """Instansiate the class."""
        self.check_arguments(**kwargs)

        if self.invalid:
            self.action = None
            return

        if project is True:
            self.all_projects(project=project, **kwargs)
            return

        if project is not None:
            self.project(project=project, **kwargs)
            return

        self.tasks(**kwargs)
        return

    def check_arguments(self, done, skip, add, **kwargs):
        """Catch conflicting arguments."""
        if done and skip:
            print("Invalid argument combination")
            self.invalid = True
            return

        if add is not None and skip:
            print("Invalid argument combination")
            self.invalid = True
            return

        if add is not None and done:
            print("Invalid argument combination")
            self.invalid = True
            return

        self.invalid = False

    def all_projects(self, task, add, **kwargs):
        """Target project level actions."""
        if add and task:
            print("Specify a target project. `Next -p -l` to list projects.")
            self.action = None
            return
        if add is not None:
            self.action = "create project"
            CreateProject(add)
            return
        ListTasks(GetTasks().file_data["projects"], "Projects")
        self.action = "list projects"
        return

    def project(self, project, task, done, skip, add, **kwargs):
        """Perform actions within a targeted project."""
        if add is not None:
            CreateProjectTask(project, add)
            self.action = "project add task"
            return
        if task:
            GetNextTaskFromProject(project)
            self.action = "project get task"
            return
        if skip:
            SkipNextTaskInProject(project)
            self.action = "project skip task"
            return
        if done:
            CloseNextTaskInProject(project)
            self.action = "project close task"
            return
        data = FindProject(project, GetTasks().file_data).data
        print("\n")
        ListTasks(data["tasks"], f"Project: {data['summary']}")
        print("\n")
        self.action = "project list tasks"
        return

    def tasks(self, task, done, skip, add, **kwargs):
        """Perfrom actions against the main task list."""
        if task:
            GetNextTask().print_task()
            self.action = "get task"
            return
        if add is not None:  # TODO: Fix this
            task_data = TaskData()
            task = CreateTask(task_data.task_count, add)
            task_data.tasks.append(task.__dict__)
            WriteTask(task_data.__dict__)
            Format(task.__dict__).create_task()
            self.action = "create task"
            return
        if done:
            MarkAsClosed()
            self.action = "close task"
            return
        if skip:
            SkipTask()
            self.action = "skip task"
            return
        ListTasks(GetTasks().file_data["tasks"])
        self.action = "list task"
