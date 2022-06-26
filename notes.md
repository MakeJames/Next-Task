# Next Task notes

## CLI Todo list

- [ ] Next -r --remove >> Remove a given task 
- [ ] Next -p --project >> add a project, if used with add then attributes that project with that task
- [ ] Next -d --due >> Set due date on creation in days
- [ ] Next [-t, -p] -l --list >> lists tasks (default 10) takes an integer as an optional argument
- [ ] Next [Options] --all >> affects all
- [ ] Next -c --config >> Creates / edits the config file

## House keeping

- [ ] Make Current task statefull

## 1.0.0

- [x] Next -v --version >> Return version >> 0.0.0
- [x] Next -a --add >> Create a task >> 0.1.0
- [x] Next -t --task >> return the next task
- [x] Next -s --skip >> skip this task and add 3 days to the due date
- [x] Next -d --done >> mark the task as done
- [x] Write a template function
- [x] Store completed tasks in a seperate list
- [x] Store last task id as a called out value
- [x] Create a Clean-up function to handle updates -- runs on writing to the task file.

## Future considerations

- Config file, to manage defaults like due date, default file location
- A postpone function to defer beyond your usual list.