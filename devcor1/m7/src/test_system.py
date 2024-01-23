#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using pytest for simple system testing to interact
with dockerized web servers within a CI/CD pipeline.
"""

import requests
import pytest
from bs4 import BeautifulSoup


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
    # Also need Referer for CSRF to function correctly
    kwargs["headers"].update(
        {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": kwargs["url"],
        }
    )

    # Need to use a session to retain cookie state (helps with CSRF)
    sess = requests.session()

    # Issue GET request to get the CSRF token
    get_resp = sess.get(**kwargs)
    assert get_resp.status_code == 200

    # Parse the CSRF token from the HTML body text
    soup = BeautifulSoup(get_resp.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf_token"})
    csrf_token = csrf["value"]

    # Assemble the data string which contains the CSRF token and
    # the account ID to query
    data = f"csrf_token={csrf_token}&acctid={acct['acctid']}"

    # Issue the POST request using the custom data string and updated headers
    post_resp = sess.post(**kwargs, data=data)
    assert post_resp.status_code == 200

    # Perform checks to ensure the account balance is correct
    # If the account is invalid, ensure the proper message is displayed
    balance = acct.get("acctbal")
    if balance:
        assert f"Account balance: {balance}" in post_resp.text
    else:
        assert "Unknown account number" in post_resp.text
