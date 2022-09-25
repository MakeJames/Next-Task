# CHANGELOG

## 0.4.0
Major refactor of logic models, moving task storage into an sqlite database.
Moving the task storage into a database simplies much of the implementation and enables the creation of pojects

### Breaking changes
- previously created tasks will be lost

### Major changes:
- Seamless setup of a task database and required tables on startup

### Minor changes:
- task addition, fetching, skipping and closing are mutually exclusive activities and are now handled natively in argparse.
- Whilst entire logic model has been written functionality should be much the same

### TODO:

### Store Functions
- [ ] Establish if file exists if not create and setup schema
- [ ] Establish if the database is on the latest version - if not update

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
