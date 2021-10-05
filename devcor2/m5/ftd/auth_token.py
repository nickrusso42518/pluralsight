#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Provides common authentication process for other
scripts in this demo.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import requests


def get_token(api_path):
    """
    Gets a bearer token from Cisco FTD (FDM API). Returns the token
    string if successful; raises HTTPError otherwise.
    """

    # The FTD sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # To authenticate, we issue a POST request with our username/password
    # as a JSON body to obtain a bearer token in response.
    post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # This is the JSON payload included in the initial POST request to
    # obtain a bearer token.
    token_data = {
        "grant_type": "password",
        "username": "admin",
        "password": "Cisco1234",
    }

    # Issue the POST request to the proper URL with the predefined headers
    # and body dictionaries. Be sure to ignore SSL cert checking as this
    # is a standalone sandbox FTD instance.
    token_resp = requests.post(
        f"{api_path}/fdm/token",
        headers=post_headers,
        json=token_data,
        verify=False,
    )
    token_resp.raise_for_status()

    # We've obtained the bearer token; return it
    bearer_token = token_resp.json()["access_token"]
    return bearer_token


def main():
    """
    Execution begins here.
    """

    # Tested using the FTD DevNet sandbox
    token = get_token("https://10.10.20.65/api/fdm/latest")
    print(token)


if __name__ == "__main__":
    main()
