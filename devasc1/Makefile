.DEFAULT_GOAL := all

.PHONY: all
all:	fmt lint

.PHONY: fmt
fmt:
	@echo "Starting  format"
	find . -name "*.py" | xargs black --line-length 80
	@echo "Completed format"

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs pylint
	find . -name "*.yml" | xargs yamllint -s
	@echo "Completed lint"
