# Next-task

A barebones task management solution. 

## About
Tasks are stored in a json file stored in the users Home directory `.tasks.json`. This file is updated and managed by various functions within the package.

## Getting Started

```bash
git clone git@gitlab.com:mcbean-workspace/next-task.git
cd next-task
make 
Next --version
```

## Development

```bash
git clone git@gitlab.com:mcbean-workspace/next-task.git
cd next
make dev
export LOG_LEVEL=INFO # Optional: supports DEBUG, WARNING
poetry run Next --version
```

New functionality should be made on a feature branch `feature/feature_name` and merged to `main` 


### Versioning

```bash
poetry version
```

Version increments are definbed as Major.Minor.Patch

Don't forget to update
- pyproject.toml
- next_tasks/\_\_init__.py
- VERSION

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
