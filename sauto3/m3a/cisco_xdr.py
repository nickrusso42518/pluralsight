#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple SDK to abstract Cisco Extended Detection and Response (XDR)
API requests.
"""

import requests


class CiscoXDR:
    """
    Definition of XDR API wrapper.
    """

    def __init__(self, client_id, client_secret, scope, domain="amp.cisco.com"):
        """
        Constructor takes in the XDR domain, scope, and HTTP basic
        auth client_id/client_secret. This method also issues a request to
        obtain an OAuth2 token for subsequence requests. If no domain is
        supplied, method uses the North American region.
        """

        # Retain supplied host and auth creds, then create a new session
        self.base_url = f"https://visibility.{domain}/iroh"
        self.sess = requests.session()

        # Use highly-customized POST request to get access token. Body is
        # webform data and it uses HTTP basic auth, unlike subsequent calls.
        auth_resp = self.sess.post(
            f"{self.base_url}/oauth2/token",
            auth=(client_id, client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "scope": scope,
            },
        )

        # Check for errors and extract the JSON data
        auth_resp.raise_for_status()
        auth_data = auth_resp.json()
        token_type = auth_data["token_type"].capitalize()  # "bearer"
        token_value = auth_data["access_token"]

        # Build the header dict to include the new token
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{token_type} {token_value}",
        }

    @staticmethod
    def make_devnet_client():
        """
        Static method to return a new CiscoXDR instance using hardcoded
        DevNet learning lab defaults for client_id, client_secret, and scope.
        These values may change over time, so check this link for updates:
        https://developer.cisco.com/docs/cisco-xdr
        """

        # Scopes identified by DevNet at this time
        permissions = [
            "integration:read",
            "private-intel:read",
            "profile:read",
            "inspect:read",
            "users:read",
            "invite:read",
            "enrich:read",
            "oauth:read",
            "response:read",
            "global-intel:read",
            "ao:read",
        ]

        # Return new CiscoXDR instance
        return CiscoXDR(
            client_id="client-546e34fc-c6bf-4951-ac69-f6d7987a7814",
            client_secret="MYw4_E_tBdFwUwrX6WFYKVD5LQrG2k7XrJ5J046wWE0s1gAKCxJ8VA",
            scope=" ".join(permissions),
        )

    def req(self, resource, method="get", jsonbody=None):
        """
        Issues a generic HTTP request to a given resource and with given
        keyword arguments. Returns the body of the response, if it exists,
        as Python objects.
        """

        # Issue the generic HTTP request using the object's session attribute
        resp = self.sess.request(
            url=f"{self.base_url}/{resource}",
            method=method,
            headers=self.headers,
            json=jsonbody,
        )

        # If any errors occurred (status code >= 400), raise an HTTPError
        resp.raise_for_status()

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            # import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}


if __name__ == "__main__":

    # Create a new XDR instance with default (DevNet LL) parameters
    xdr = CiscoXDR.make_devnet_client()

    # Get user ID to ensure API is working
    user_data = xdr.req("profile/whoami")
    print(f"User ID: {user_data['user']['user-id']}")
