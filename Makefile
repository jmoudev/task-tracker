APP=tasks
UV=uv
RUN=$(UV) run
PYTHON=python
LINT=ruff
TYPE_CHECK=mypy

.PHONY: help install install-dev lint type-check test test-all

help:
	@echo "Printing helpers"
	$(RUN) $(APP) --help

# TODO: Install a only the project of packages, and necessary deps
install:
	@echo "Installing project"
	$(UV) sync

install-dev:
	@echo "Installing project in dev mode"
	$(UV) sync --group dev
	$(RUN) pre-commit install

lint:
	@echo "Linting"
	$(RUN) --group lint $(LINT) format .

type-check:
	@echo "Type checking"
	$(RUN) --group type $(TYPE_CHECK) .

test:
	$(RUN) --group test pytest

test-all:
	$(RUN) --group test tox run-parallel
