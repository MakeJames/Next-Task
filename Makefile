SHELL=/bin/bash
EXECUTE=poetry run
VERSION=$$(cat next_task/VERSION)

# code
PACKAGE=next_task

# file groups
TEST_GROUP=tests/*/test_*.py
LINT_GROUP=$(PACKAGE)
CLEAN_GROUP=$(PACKAGE) tests/

# targets
## standard
all: build

install:
	python3 -m pip install ./dist/$(PACKAGE)-$(VERSION)-py3-none-any.whl

uninstall:
	python3 -m pip uninstall $(PACKAGE)

clean:
	rm -rf dist

info:

check: format lint test

## less standard
dev:
	poetry install
	poetry env use python3
	cp pre-commit .git/hooks/

pre-commit: lint

format:
	$(EXECUTE) isort $(LINT_GROUP)

lint:
	$(EXECUTE) pycodestyle $(LINT_GROUP) $(TEST_GROUP)
	$(EXECUTE) pydocstyle $(LINT_GROUP) $(TEST_GROUP)
	$(EXECUTE) mypy $(LINT_GROUP)

test:
	$(EXECUTE) pytest $(TEST_GROUP) -v --durations=0 --sw

coverage:
	$(EXECUTE) pytest --cov=$(PACKAGE) $(TEST_GROUP) --cov-report term-missing

build:
	poetry build

fresh: clean dev
	poetry update
