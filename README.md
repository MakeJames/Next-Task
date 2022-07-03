# Next-task

A barebones task management solution for those that have far too much to do.

## About

Install by running `python3 -m pip install git+https://github.com/MakeJames/Next-Task.git`

### Tasks

Tasks are a descrete unit of work that needs to be done, such as:

* `email Fred the stats from last quarter`
* `read the article about bees`

Tasks can be added to the list of tasks at any stage, with `Next -a [summary]`. When 
requested with `Next -t` the list of tasks is prioritied and the next highest priotiy 
task is returned to the user. This task can then be actioned to completeion and marked 
as complete with `Next -d`. 

For whatever reason the "next" task can be skipped with `Next -s`, which will add time
to the due date which will reduce it's priority. Bear in mind that older tasks will come 
up with more frequency than newer tasks.

The next task is stateful, so when you have an active task it will remain the next task, 
until it is completed. This means that if new tasks are added whilst actioning a task, 
the current task will remain the same until completed or skipped.

Use `Next -l` to view a complete list of open tasks.


## Development

```bash
git clone git@gitlab.com:mcbean-workspace/next-task.git
cd next
make dev
poetry run Next --version
```

New functionality should be made on a feature branch `feature/feature_name` and merged to `main` 

```mermaid
%%{ init: { 'logLevel': 'debug', 'theme': 'neutral', 'gitGraph': { 'mainBranchOrder': 1 } }%%
    gitGraph
        commit id: "INIT"
        branch feature/feature_name order:3
        checkout feature/feature_name
        commit
        commit
        checkout main
        merge feature/feature_name tag: "0.1.0"
        branch feature/another_feature order:4
        checkout feature/another_feature
        commit
        checkout main
        branch fix/resolve_issue order: 2
        checkout fix/resolve_issue
        commit
        checkout main
        merge fix/resolve_issue tag: "0.1.1"
        checkout feature/another_feature
        commit
        merge main
        checkout main
        merge feature/another_feature tag: "0.2.0"
```


### Versioning

```bash
poetry version
```

Version increments are definbed as Major.Minor.Patch

Don't forget to update
- pyproject.toml
- next_tasks/VERSION

### Lint and Test

Code should be complient with PEPs 8, 256, 484 and 526.
Unit test coverage should be 85% or higher.

```bash
make check # calls make lint; make test
make coverage # returns the coverage report
```

### Commit Messages

Commit messages are prefixed with the following stubs

```bash
INIT # structural changes to pakage contents
FUNC # functional changes
DOCS # documentation
TEST # commits adding tests to the repository
LINT # corrections to formatting or spelling
REFACTOR # Non functional changes to functions improving performance or readability
```

### Structure

dev tools come with code2flow, can generate an up-to-date structure diagram with `code2flow -o docs/class_diagram.png -q next_task/`

```mermaid
stateDiagram-v2
    state next_task {
        # direction LR
        [*] --> task:--task
        [*] --> add:--add
        [*] --> list:--list
        [*] --> skip:--skip
        [*] --> done:--done
        state interface {
            state cli {
                task --> GetNextTask
                add --> CreateTask
                list --> GetNextTask
                skip --> SkipTask
                done --> MarkAsClosed
            }
            state console_output {
                GetNextTask --> ListTasks
                CreateTask --> Format
                GetNextTask --> Format
                SkipTask --> Format
                MarkAsClosed --> Format
                GetNextTask --> Congratulations
            }
        }
        state services {
            state Store {
                CreateTask --> WriteTask
                WriteTask --> CheckTaskStore
                WriteTask --> CheckFormatting
                GetTasks
                CreateTask --> GetTasks
                GetNextTask --> GetTasks
                GetTasks --> CheckTaskStore
                GetTasks --> CheckFormatting
                GetTasks --> CreateTask
                GetTasks --> GetNextTask
                CheckTaskStore
                CheckFormatting
            }
            state Task {
                GetNextTask
                GetPriority
                GetNextTask --> GetPriority
                GetPriority --> GetNextTask
                SkipTask --> GetNextTask
                MarkAsClosed --> GetNextTask
                SkipTask
                MarkAsClosed
                CreateTask
            }
        }
    
    }
```
