# 'make' by itself runs the 'all' target
.DEFAULT_GOAL := all

.PHONY: all
all: lint run

.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: lint
lint:
	find . -name "*.yml" | xargs ansible-lint

.PHONY: run
run:
	ansible-playbook build_lab.yml
