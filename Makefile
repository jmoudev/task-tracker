PYTHON=python

.PHONY: help
help:
	@echo "Printing helpers"
	task-cli --help

.PHONY: install
install:
	@echo "Installing project"
	$(PYTHON) -m pip install .

.PHONY: install-dev
install-dev:
	@echo "Installing project in dev mode"
	pre-commit install
	$(PYTHON) -m pip install -e .[dev]

.PHONY: test
test:
	$(PYTHON) -m unittest discover tests
