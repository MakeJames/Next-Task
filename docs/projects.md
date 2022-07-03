# Next task: Projects

Projects are a large task, they can be long running or have defined scope and completed. Unlike tasks, 
projects are not prioritised by due date, but are user selected. 

Within each project there is a defined task list and when there is an active project, next tasks will be 
returned from the project tasks.

Task creation should remain unaffected, so even when there is a defined 'current' project, new tasks will 
default to the general task list.

If a current project is set, the need to provide a project key is redundant.


## TODO

* [ ] list projects
* [ ] set project as current
* [ ] create task in project
* [ ] complete task in project
* [ ] skip task in project
* [ ] if in project then set project

## Options

```mermaid
%%{ init: {"logLevel": 1, "theme": "dark", "flowchart": {"defaultRenderer": "dagre-wrapper}} }%%
graph LR
    subgraph projects
    1(["Next --project"]) --> B(specify the project group of tasks)
    2(["Next --project --add [summary]"]) --> C(Create a project)
    8(["Next --project [project key]"]) --> I(Sets given project as current project) 
    end
    subgraph tasks
    3(["Next --project [project key] --add --task"]) --> D(Create a task in a specified project)
    4(["Next --project [project key] --task"]) --> E(Return the next task in a project)
    5(["Next --project [project key] --task --done"]) --> F(Close the next priority task in a project)
    6(["Next --project [project key] --task --skip"]) --> G(Skip the next priority task in a project)
    end
    subgraph other
    7(["Next --project --list"]) --> H(List the projects and their key)
    end
```

