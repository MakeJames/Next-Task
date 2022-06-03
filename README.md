# Next-task

A barebones task management solution

## About
Tasks are stored in a json file stored in the users Home directory `.tasks.json`. This file is updated and managed by various functions within the package.

## Getting Started

```bash
git clone git@gitlab.com:{}
cd next-task
make 
Next --version
```

## Development

```bash
git clone git@gitlab.com:{}
cd next
git check out dev
make dev
export LOG_LEVEL=INFO # Optional: supports DEBUG, ERROR
poetry run Next --version
```

### Versioning

```bash
poetry version
```

Version increments are definbed as Major.Minor.Patch

Don't forget to update
- pyproject.toml
- VERSION

### Lint and Test

Code should be complient with PEPs 8, 256, 484 and 526.
Unit test coverage should be 85% or higher.

```bash
make check # calls make lint; make test
make coverage # returns the coverage report
```

## Concept

```json
{
    "tasks": [
        {
            "id": 1,
            "summary": "A short Description",
            "created": "timestamp",
            "due": "timestamp",
            "status": "open/closed"
        },
        {
            "id": 2,
            "summary": "A short Description",
            "created": "timestamp",
            "due": "timestamp",
            "status": "open/closed"
        }
    ]
}
```