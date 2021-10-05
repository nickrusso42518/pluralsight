# 'make' by itself runs the 'all' target
.DEFAULT_GOAL := all

.PHONY: all
all:	fmt lint test

.PHONY: fmt
fmt:
	@echo "Starting  format"
	find . -name "*.py" | xargs black --line-length 80
	@echo "Completed format"

# remove yamllint before video and publication
.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs pylint
	@echo "Completed lint"

.PHONY: test
test:
	@echo "Starting  unit tests"
	find . -name "*.pyc" -delete
	pytest .
	@echo "Completed unit tests"
