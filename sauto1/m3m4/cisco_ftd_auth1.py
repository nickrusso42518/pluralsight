#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Python client SDK for Cisco FTD.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import requests

class CiscoFTD:
    """
    Python client SDK for Cisco FTD.
    """

    def __init__(
        self,
        host="10.10.20.65",
        username="admin",
        password="Cisco1234",
        verify=False,
    ):
        """
        Constructor for the class. Takes in optional hostname/IP, username,
        password, and optional SSL verification setting. If left blank,
        the reservable DevNet sandbox will be used by default.
        """

        # Store all input parameters and assemble the base URL
        self.username = username
        self.password = password
        self.verify = verify
        self.api_path = f"https://{host}/api/fdm/latest"

        # If we aren't verifying SSL certificates, disable obnoxious warnings
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a stateful HTTPS session to improve performance
        self.sess = requests.session()

        # To authenticate, we issue a POST request with our username/password
        # as a JSON body to obtain a bearer token in response. These headers
        # are reusable because almost all API interactions use JSON
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Perform initial authentication
        self.authenticate("password")

    #
    # General management methods/utilities
    #

    def authenticate(self, grant_type):
        """
        Perform authentication, either initial or refresh, and retain the new
        tokens as attributes of the object.
        """

        # This is the JSON payload included in the initial POST request to
        # obtain a bearer token.
        token_data = {"grant_type": grant_type}
        if grant_type == "refresh_token":
            token_data["refresh_token"] = self.refresh_token
        elif grant_type == "password":
            token_data.update(
                {"username": self.username, "password": self.password}
            )

        # Issue the POST request to the proper URL with the predefined headers
        # and body dictionaries. Be sure to ignore SSL cert checking as this
        # is a standalone sandbox FTD instance.
        token_resp = self.sess.post(
            f"{self.api_path}/fdm/token",
            headers=self.headers,
            json=token_data,
            verify=self.verify,
        )
        token_resp.raise_for_status()

        # We've obtained the token data; extract the critical values
        token_data = token_resp.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]

        # Update the headers dictionary with the new access token
        self.headers["Authorization"] = f"Bearer {self.access_token}"

    def reauthenticate(self):
        """
        Uses the 'refresh_token' to reauthenticate the session to FTD.
        """
        self.authenticate("refresh_token")


def main():
    """
    Quickly test the FTD class authentication capabilities.
    """

    # Create a new FTD object, which performs initial auth; show the tokens
    ftd = CiscoFTD()
    print("First access token")
    print(ftd.access_token)
    print("First refresh token")
    print(ftd.refresh_token)

    # Reauthenticate using the refresh token; show the tokens
    ftd.reauthenticate()
    print("Second access token")
    print(ftd.access_token)
    print("Second refresh token")
    print(ftd.refresh_token)


if __name__ == "__main__":
    main()
