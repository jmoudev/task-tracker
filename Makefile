APP=tasks
RUN=uv run
PYTHON=python

.PHONY: help install dev lint type-check test test-all

help:
	@echo "Printing helpers"
	$(RUN) $(APP) --help

install:
	@echo "Basic install"
	uv venv
	uv pip install .

dev:
	@echo "Installing project in dev mode"
	uv sync --group dev
	$(RUN) pre-commit install

lint:
	@echo "Linting"
	$(RUN) --group lint ruff check . --fix

type-check:
	@echo "Type checking"
	$(RUN) --group type mypy .

test:
	$(RUN) --group test pytest --cov=src tests

test-all:
	$(RUN) --group test tox run-parallel
