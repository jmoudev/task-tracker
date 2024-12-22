APP=tasks
PYTHON=python
LINTER=ruff
TYPE_CHECKER=mypy

.PHONY: help install install-dev lint type-check test

help:
	@echo "Printing helpers"
	$(APP) --help

install:
	@echo "Installing project"
	$(PYTHON) -m pip install .

install-dev:
	@echo "Installing project in dev mode"
	$(PYTHON) -m pip install -e .[dev]
	pre-commit install

lint:
	@echo "something"
	$(LINTER) format .

type-check:
	@echo "type checking"
	$(TYPE_CHECKER) .

test:
	$(PYTHON) -m unittest discover tests
