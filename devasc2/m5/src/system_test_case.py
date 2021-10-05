#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
This is an alternative to pytest which uses many Java idioms.
"""


from unittest import TestCase
import requests


class SystemTestCase(TestCase):
    """
    Defines a test case for the full system test.
    """

    def test_get_good_page(self):
        """
        Simulate a user navigating to the website with an HTTP GET.
        """
        get_headers = {"Accept": "text/html"}
        for port in [5001, 5002, 5003]:
            resp = requests.get(f"http://localhost:{port}", headers=get_headers)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Enter account ID", resp.text)

    def test_get_bad_page(self):
        """
        Simulate a user navigating to an invalid URL with an HTTP GET.
        """
        get_headers = {"Accept": "text/html"}
        for port in [5001, 5002, 5003]:
            resp = requests.get(
                f"http://localhost:{port}/bad.html", headers=get_headers
            )
            self.assertEqual(resp.status_code, 404)
            self.assertIn("Not Found", resp.text)

    def test_post_good_acct(self):
        """
        Simulate a user entering a valid account number and clicking "Submit"
        """
        self._post_acct({"acctid": "ACCT100", "acctbal": "40.00 USD"})

    def test_post_bad_acct(self):
        """
        Simulate a user entering an invalid account number and clicking "Submit"
        """
        self._post_acct({"acctid": "nick123"})

    def _post_acct(self, acct):
        post_headers = {
            "Accept": "text/html",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        for port in [5001, 5002, 5003]:
            resp = requests.post(
                f"http://localhost:{port}",
                headers=post_headers,
                data=f"acctid={acct['acctid']}",
            )
            self.assertEqual(resp.status_code, 200)
            balance = acct.get("acctbal")
            if balance:
                self.assertIn(f"Account balance: {balance}", resp.text)
            else:
                self.assertIn("Unknown account number", resp.text)
