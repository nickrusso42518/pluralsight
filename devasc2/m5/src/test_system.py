#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using pytest for simple system testing to interact
with dockerized web servers within a CI/CD pipeline.
"""

import requests


def test_get_good_page():
    """
    Simulate a user navigating to the website with an HTTP GET.
    """
    get_headers = {"Accept": "text/html"}
    for port in [5001, 5002, 5003]:
        resp = requests.get(f"http://localhost:{port}", headers=get_headers)
        assert resp.status_code == 200
        assert "Enter account ID" in resp.text


def test_get_bad_page():
    """
    Simulate a user navigating to an invalid URL with an HTTP GET.
    """
    get_headers = {"Accept": "text/html"}
    for port in [5001, 5002, 5003]:
        resp = requests.get(
            f"http://localhost:{port}/bad.html", headers=get_headers
        )
        assert resp.status_code == 404
        assert "Not Found" in resp.text


def test_post_good_acct():
    """
    Simulate a user entering a valid account number and clicking "Submit".
    """
    _post_acct({"acctid": "ACCT100", "acctbal": "40.00 USD"})


def test_post_bad_acct():
    """
    Simulate a user entering an invalid account number and clicking "Submit".
    """
    _post_acct({"acctid": "nick123"})


def _post_acct(acct):
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
        assert resp.status_code == 200
        balance = acct.get("acctbal")
        if balance:
            assert f"Account balance: {balance}" in resp.text
        else:
            assert "Unknown account number" in resp.text
