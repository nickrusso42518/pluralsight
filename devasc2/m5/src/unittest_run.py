"""
Author: Nick Russo
Purpose: Entrypoint for unittest-based unit and system tests. For variety,
unit and system tests have been combined in one file. Just ensure you
use `(sudo) docker-compose up --detach` before running it.

"""

import unittest
from database_test_case import DatabaseTestCase
from system_test_case import SystemTestCase


def main():
    """
    Test execution starts here.
    """

    # The loader is responsible for loading test cases into test suites
    test_loader = unittest.TestLoader()

    # Build a list of test suites to run
    test_suites = [
        test_loader.loadTestsFromTestCase(DatabaseTestCase),
        test_loader.loadTestsFromTestCase(SystemTestCase),
    ]

    # The runner is responsible for executing tests and printing output
    test_runner = unittest.TextTestRunner(verbosity=2)

    # Iterate over all of the test suites, run each one in series
    for test_suite in test_suites:
        test_runner.run(test_suite)


if __name__ == "__main__":
    main()
