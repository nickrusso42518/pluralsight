#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
"""

import pytest
import database


@pytest.fixture(scope="module")
def db_mock():
    """
    Test fixture setup to create sample database from "model" data.
    """
    return database.Database("sqlite:///:memory:", "src/data/initial.json")


def test_balance(db_mock):
    """
    Test the "balance()" method.
    """
    db_mock.connect()
    assert db_mock.balance("ACCT100") == "40.00 USD"
    assert db_mock.balance("ACCT200") == "-10.00 USD"
    assert db_mock.balance("ACCT300") == "0.00 USD"
    assert db_mock.balance("nick123") is None
    db_mock.disconnect()
