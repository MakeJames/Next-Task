# CHANGELOG

## 0.4.0
Major refactor of logic models, moving task storage into an sqlite database.
Moving the task storage into a database simplies the implementation and enables the creation of pojects

### Breaking changes
- previously created tasks will be lost

### Major changes:
- Task store managed in a sqlite database stored in the `$HOME/Notes/` directory
- Seamless setup of a task database and required tables on startup

### Minor changes:
- Task addition, fetching, skipping and closing are mutually exclusive activities
- Prioirity now calculated as a delta between task_id and number of skips affecting the issue's 'rank'

### TODO:

Broadly, reimplement preiviously exisiting functionality and ensure requirements of the projects feature met.

### Store Functions
- [x] Establish if file exists if not create and setup schema
- [x] Establish if the database is on the latest version - if not update

#### Main Functions
- [x] Task addition
- [x] Task skipping
- [x] Task completion
- [x] Retrieve next task
- [ ] Create Project
- [ ] set current project
- [ ] clear current project
- [ ] when no more tasks prompt user to clear or close current project
- [ ] Declare current project

#### Streach
- [x] Refactor Console Output
- [ ] Retain task data on update