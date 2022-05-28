# Next

A barebones task management solution

## Getting Started

```bash
git clone git@gitlab.com:{}
cd next
make 
next --version
```

## Development

```bash
git clone git@gitlab.com:{}
cd next
git check out dev
make dev
export LOG_LEVEL=INFO # Optional: supports DEBUG, ERROR
poetry run next --version
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