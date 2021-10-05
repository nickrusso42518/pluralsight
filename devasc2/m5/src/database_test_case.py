#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
This is an alternative to pytest which uses many Java idioms.
"""


from unittest import TestCase
from database import Database


class DatabaseTestCase(TestCase):
    """
    Defines a test case for the Circle class.
    """

    def setUp(self):
        """
        Load data from our JSON file into memory. This is an object attribute
        so it is easily referenced in subsequent test methods.
        """
        self.db = Database("src/data/db.json")

    def test_balance(self):
        """
        Test the "balance()" method. This doesn't follow TDD since we
        wrote the code for this method a long time ago.
        """
        self.assertEqual(self.db.balance("ACCT100"), "40.00 USD")
        self.assertEqual(self.db.balance("ACCT200"), "-10.00 USD")
        self.assertEqual(self.db.balance("ACCT300"), "0.00 USD")
        self.assertIsNone(self.db.balance("nick123"))

    def test_owes_money(self):
        """
        Test the "owes_money()" method. This does follow TDD since we
        wrote this test before the method was implemented.
        """
        self.assertTrue(self.db.owes_money("ACCT100"))
        self.assertFalse(self.db.owes_money("ACCT200"))
        self.assertFalse(self.db.owes_money("ACCT300"))
        self.assertIsNone(self.db.owes_money("nick123"))
