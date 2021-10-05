#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

import json


class Database:
    """
    Represent the interface to the data (model). Can read from a
    simple file such as JSON, YAML, or XML. Uses JSON by default.
    """

    def __init__(self, path):
        """
        Constructor to initialize the data attribute as
        a dictionary where the account number is the key and
        the value is another dictionary with keys "paid" and "due".
        """

        # Open the specified database file for reading and perform loading
        with open(path, "r") as handle:
            self.data = json.load(handle)

    def balance(self, acct_id):
        """
        Determines the customer balance by finding the difference between
        what has been paid and what is still owed on the account, The "model"
        can provide methods to help interface with the data; it is not
        limited to only storing data. A positive number means the customer
        owes us money and a negative number means they overpaid and have
        a credit with us.
        """
        acct = self.data.get(acct_id)
        if acct:
            bal = float(acct["due"]) - float(acct["paid"])

            # Style added in module 4
            return f"{bal:.2f} USD"

        return None
