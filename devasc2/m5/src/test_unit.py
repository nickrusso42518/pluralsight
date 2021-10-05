#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
"""

import pytest
import database


@pytest.fixture
def db_mock():
    """
    Test fixture setup to create sample database from "model" data.
    """
    return database.Database("src/data/db.json")


def test_balance(db_mock):
    """
    Test the "balance()" method. This doesn't follow TDD since we
    wrote the code for this method a long time ago.
    """
    assert db_mock.balance("ACCT100") == "40.00 USD"
    assert db_mock.balance("ACCT200") == "-10.00 USD"
    assert db_mock.balance("ACCT300") == "0.00 USD"
    assert db_mock.balance("nick123") is None


def test_owes_money(db_mock):
    """
    Test the "owes_money()" method. This does follow TDD since we
    wrote this test before the method was implemented.
    """
    assert db_mock.owes_money("ACCT100")
    assert not db_mock.owes_money("ACCT200")
    assert not db_mock.owes_money("ACCT300")
    assert db_mock.owes_money("nick123") is None
