#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using pytest for simple system testing to interact
with dockerized web servers within a CI/CD pipeline.
"""

import requests
import pytest


@pytest.fixture()
def kwargs():
    """
    Test fixture setup to disable SSL self-signed certificate warnings.
    """
    requests.packages.urllib3.disable_warnings()
    return {
        "url": "https://localhost:5000",
        "verify": False,
        "headers": {"Accept": "text/html"},
    }


def test_get_good_page(kwargs):
    """
    Simulate a user navigating to the website with an HTTP GET.
    """
    resp = requests.get(**kwargs)
    assert resp.status_code == 200
    assert "Enter account ID" in resp.text


def test_get_bad_page(kwargs):
    """
    Simulate a user navigating to an invalid URL with an HTTP GET.
    """
    kwargs["url"] = "https://localhost:5000/bad.html"
    resp = requests.get(**kwargs)
    assert resp.status_code == 404
    assert "Not Found" in resp.text


def test_post_good_acct(kwargs):
    """
    Simulate a user entering a valid account number and clicking "Submit".
    """
    _post_acct(kwargs, {"acctid": "ACCT100", "acctbal": "40.00 USD"})
    _post_acct(kwargs, {"acctid": "ACCT200", "acctbal": "-10.00 USD"})
    _post_acct(kwargs, {"acctid": "ACCT300", "acctbal": "0.00 USD"})


def test_post_bad_acct(kwargs):
    """
    Simulate a user entering an invalid account number and clicking "Submit".
    """
    _post_acct(kwargs, {"acctid": "nick123"})


def _post_acct(kwargs, acct):
    """
    Helper function to perform a post request. Takes in the keyword
    arguments (basic site data) and the account data to check.
    """

    # Need additional headers, content-type typically need for POSTs
    kwargs["headers"].update(
        {"Content-Type": "application/x-www-form-urlencoded"})

    resp = requests.post(**kwargs, data=f"acctid={acct['acctid']}")
    assert resp.status_code == 200

    # Perform checks to ensure the account balance is correct
    # If the account is invalid, ensure the proper message is displayed
    balance = acct.get("acctbal")
    if balance:
        assert f"Account balance: {balance}" in resp.text
    else:
        assert "Unknown account number" in resp.text
