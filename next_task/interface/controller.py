"""Manage the methods of the cli arguments."""

from next_task.interface.console_output import Format, ListTasks
from next_task.services.projects import (CloseNextTaskInProject, CreateProject,
                                         CreateProjectTask, FindProject,
                                         GetNextTaskFromProject,
                                         SkipNextTaskInProject)
from next_task.services.store import Tasks, WriteTask
from next_task.services.tasks import (CreateTask, GetNextTask, MarkAsClosed,
                                      SkipTask, TaskData)


# TODO: Implement the following folow
# 1: Get file data
# 2. Run Argument updates
# 3. Print Update
# 4. Write file

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
        ListTasks(Tasks().file_data["projects"], "Projects")
        self.action = "list projects"
        return

    def project(self, project, task, done, skip, add, **kwargs):
        """Perform actions within a targeted project."""
        if add is not None:
            CreateProjectTask(project, add, TaskData())
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
        data = FindProject(project, TaskData()).data
        print("\n")
        ListTasks(data["tasks"], f"Project: {data['summary']}")
        print("\n")
        self.action = "project list tasks"
        return

    def tasks(self, task, done, skip, add, **kwargs):
        """Perfrom actions against the main task list."""
        # TODO: Get TaskData here
        if add is not None:  # TODO: Fix this
            task_data = TaskData()
            task = CreateTask(task_data.task_count, add)
            task_data.tasks.append(task.__dict__)
            task_data.task_count = task.id
            WriteTask(task_data.__dict__)
            Format(task.__dict__).create_task()
            self.action = "create task"
            return
        tasks = GetNextTask()
        if task:
            tasks.print_task()
            self.action = "get task"
            return
        if done:
            close = MarkAsClosed(tasks.task_data)
            self.action = "close task"
            Format(close.closed_task).mark_closed()
            GetNextTask()
            GetNextTask(close.task_data).print_task()
            return
        if skip:
            skip = SkipTask(tasks.task_data)
            self.action = "skip task"
            Format(skip.skip_task).skip_task()
            # TODO: Validate that the next task != skip.skip_task
            GetNextTask(skip.task_data).print_task()
            return
        ListTasks(tasks.task_data.tasks)
        self.action = "list task"
