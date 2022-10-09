# CHANGELOG

## 0.4.0
*2022-10-09*

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

### Store Functions
- [x] Establish if file exists if not create and setup schema
- [x] Establish if the database is on the latest version
- [x] Manage Database conections within a context manager to gracefuly close connections
- [x] Wrap DB connections to read or write functions with reutrns tailored to the function.

#### Main Functions
- [x] Task addition
- [x] Task skipping
- [x] Task completion
- [x] Retrieve next task
- [x] Create Project
- [x] set current project
- [x] clear current project
- [x] Declare current project

#### Streach
- [x] Refactor Console Output
- [x] Dynamic project lookup to find projects in the db

### Descoped
- [ ] Retain task data on update
- [ ] when no more tasks prompt user to clear or close current project