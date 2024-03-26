#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Provides Batfish with the "snapshot_name" input
option and corresponding fixture for use in tests.
"""

import pytest


def pytest_addoption(parser):
    """
    Hook function to enable pytest to consume CLI arguments. Specifically,
    it allows operators to specify the name of the Batfish snapshot.
    """
    parser.addoption("--snapshot_name", action="store")


@pytest.fixture(scope="session")
def snapshot_name(request):
    """
    Treat the snapshot_name as a fixture so it is accessible within the
    test functions that require it.
    """
    return request.config.option.snapshot_name
