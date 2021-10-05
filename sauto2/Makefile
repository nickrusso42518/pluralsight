# Default goal runs the "test" target
.DEFAULT_GOAL := all

.PHONY: all
all: lint unit clean

.PHONY: lint
lint:
	@echo "Starting  lint"
	find . -name "*.py" | xargs pylint
	find . -name "*.py" | xargs black -l 82 --check
	@echo "Completed lint"

.PHONY: unit
unit:
	@echo "Starting  unit tests"
	python m2/get_computers.py
	python m3/get_samples.py
	python m4/get_site_activity.py www.internetbadguys.com
	(cd m4 && python post_sample_events.py)
	python m4/investigate_domain.py www.internetbadguys.com
	@echo "Completed unit tests"

.PHONY: clean
clean:
	@echo "Starting  clean"
	# find . -name "*.pyc" | xargs -r rm
	find . -name "*.pyc" | xargs rm
	rm -f site_activity_www_internetbadguys_com.csv
	rm -rf domain_details
	@echo "Completed clean"
