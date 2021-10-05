#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get an access token
from Cisco DNA Center using the REST API.
"""

import requests


def get_token(host):
    """
    Gets an access token from Cisco DNA Center. Returns the token
    string if successful; raises HTTPError otherwise.
    """

    # Declare useful local variables to simplify request process
    auth = ("devnetuser", "Cisco123!")
    headers = {"Content-Type": "application/json"}

    # Issue HTTP POST request to the proper URL to request a token
    auth_resp = requests.post(
        f"https://{host}/dna/system/api/v1/auth/token",
        auth=auth,
        headers=headers,
    )

    # If successful, print token. Else, raise HTTPError with details
    auth_resp.raise_for_status()
    token = auth_resp.json()["Token"]
    return token


def main():
    """
    Execution begins here.
    """

    # Use the always-on sandbox as a quick test
    token = get_token("sandboxdnac2.cisco.com")
    print(token)


if __name__ == "__main__":
    main()
