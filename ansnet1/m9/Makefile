# 'make' by itself runs the 'run' target
.DEFAULT_GOAL := run

.PHONY: run
run: lint unit iac

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.yml" | xargs ansible-lint
	find . -name "*.py" | xargs pylint
	@echo "Completed lint"

.PHONY: unit
unit:
	@echo "Starting  unit tests"
	ansible-playbook tests/unittest.yml
	@echo "Completed unit tests"

.PHONY: iac
iac:
	@echo "Starting  infra as code"
	ansible-playbook full_iac.yml
	@echo "Completed infra as code"
