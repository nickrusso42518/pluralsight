# Module 5 - Getting Familiar with DevOps Processes and Tools
This directory builds on the Module 4 code which includes several
Docker-related and CRM-app related content. The additions are
discussed below. Note that the `setup/` directory has been
removed as it is assumed that Docker and `docker-compose` are
still installed from the previous module.

## Tests
This module introduced linting, unit tests, and system tests.
  * `.pylintrc`: The configuration file used by `pylint`, a Python
    syntax and styling checker.
  * `src/test_unit.py`: Set of unit tests to evaluate the `Database`
    class `balance()` and `owes_money()` methods. This latter method
    was added using test-driven development (TDD).
  * `src/test_system.py`: Set of system tests which uses `docker-compose`
    to set up several containers then uses Python `requests` to test
    the complete functionality of all running containers.

## Test Pipeline
The course demonstrated Travis CI at a high-level to illustrate how
all the pieces fit together. The `.travis.yml` file contains the "script"
that Travis will follow upon every `git push` or pull request (PR)
operation.

## Using unittest Instead of pytest
I've included an alternative implementation of the `pytest` examples
in the course using the `unittest` library. The files relevant to this
alternative are shown below. 

```
$ tree src    
src/
|-- database_test_case.py
|-- system_test_case.py
|-- unittest_logs
|   |-- fail_log.txt
|   `-- pass_log.txt
`-- unittest_run.py
```

The files in `unittest_logs/` directory just capture the output from running
`unittest_run.py`. I show both successful and failed (TDD-based) runs.
The `*_test_case.py` files inherit from `unittest.TestCase` which provides
the backend `assert` methods, setup, teardown, and other basic features.
The `unittest_run.py` is the main script which uses a variety of
auxiliary `unittest` components to build and execute test suites.
