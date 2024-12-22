PYTHON=py

help:
	@echo "Printing helpers"
	task-cli --help

install:
	@echo "Installing project"
	$(PYTHON) -m pip install .

install-dev:
	@echo "Installing project in dev mode"
	pre-commit install
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m unittest discover tests
