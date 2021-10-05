# Author: Nick Russo
# Purpose: Provide simple "make" targets for developers
# See README for details about each target.

.DEFAULT_GOAL := all

.PHONY: all
all: clean lint

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.yaml" | xargs yamllint -s
	find . -name "*.py" | xargs pylint
	@echo "Completed lint"

.PHONY: black
black:
	@echo "Starting  black"
	find . -name "*.py" | xargs black -l 80
	@echo "Completed black"

.PHONY: clean
clean:
	@echo "Starting  clean"
	find . -name "*.pyc" | xargs rm
	@echo "Starting  clean"
