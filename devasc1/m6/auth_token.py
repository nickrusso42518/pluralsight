#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get an access token
from Cisco DNA Center using the REST API.
"""

import requests


def get_token():
    """
    Gets an access token from Cisco DNA Center. Returns the token
    string if successful; raises HTTPError otherwise.
    """

    # Declare useful local variables to simplify request process
    api_path = "https://sandboxdnac.cisco.com/dna"
    auth = ("devnetuser", "Cisco123!")
    headers = {"Content-Type": "application/json"}

    # Issue HTTP POST request to the proper URL to request a token
    auth_resp = requests.post(
        f"{api_path}/system/api/v1/auth/token", auth=auth, headers=headers
    )

    # If successful, print token. Else, raise HTTPError with details
    auth_resp.raise_for_status()
    token = auth_resp.json()["Token"]
    return token


def main():
    """
    Execution begins here.
    """

    token = get_token()
    print(token)


if __name__ == "__main__":
    main()
