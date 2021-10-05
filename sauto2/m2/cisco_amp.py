#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco AMP Cloud
to simplify API interactions.
"""

from cisco_endpoint_base import CiscoEndpointBase


class CiscoAMP(CiscoEndpointBase):
    """
    Declaration of Cisco AMP SDK class.
    """

    def __init__(self, client_id, api_key):
        """
        Constructor to create a new object. AMP uses HTTP basic auth
        so the constructor requires a client_id and api_key.
        """

        # Call the base class constructor to pass in the base URL
        super().__init__(base_url="https://api.amp.cisco.com/v1")

        # Store the HTTP basic auth parameters in a 2-tuple for use later
        self.auth = (client_id, api_key)

    def req(self, resource, **kwargs):
        """
        Issues a generic HTTP request to a specific resource using the parent
        base_url() functionality. Any other keyword arguments are
        transparently passed through. Returns the HTTP response body
        as JSON (Python objects) or an empty dicitonary if no body exists.
        """

        # Call the base_req method and include the HTTP basic auth tuple
        resp = super().base_req(resource, auth=self.auth, **kwargs)

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            # import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}

    @staticmethod
    def build_from_env_vars():
        """
        Static class-level helper method to quickly create a new CiscoAMP
        object using environment variables:
          1. AMP_CLIENT_ID: Your personal client ID (username) for AMP
          2. AMP_API_KEY: Your personal API key (password) for AMP
        """

        client_id, api_key = CiscoEndpointBase.load_env_vars(
            "AMP_CLIENT_ID", "AMP_API_KEY"
        )
        return CiscoAMP(client_id, api_key)
