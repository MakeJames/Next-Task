# CHANGELOG

## 0.4.0
Major refactor of logic models, moving task storage into an sqlite database.
Moving the task storage into a database simplies much of the implementation and enables the creation of pojects

### Breaking changes
- previously created tasks will be lost

### Major changes:
- Task store managed in a sqlite database stored in the `$HOME/Notes/`
- Seamless setup of a task database and required tables on startup

### Minor changes:
- Task addition, fetching, skipping and closing are mutually exclusive activities

### TODO:

### Store Functions
- [x] Establish if file exists if not create and setup schema
- [x] Establish if the database is on the latest version - if not update
- [ ] Retain task data on update

#### Main Functions
- [ ] Task addition
- [ ] Task skipping
- [ ] Task completion
- [ ] Retrieve next task
- [ ] set current project
- [ ] clear current project
- [ ] when no more tasks prompt user to clear or close current project

#### Streach
- [ ] Refactor Console Output
