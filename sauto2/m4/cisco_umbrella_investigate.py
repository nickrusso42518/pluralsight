#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around the Cisco Umbrella Investigate API
to simplify API interactions.
"""

from cisco_endpoint_base import CiscoEndpointBase


class CiscoUmbrellaInvestigate(CiscoEndpointBase):
    """
    Declaration of Cisco Umbrella Investigate SDK class.
    """

    def __init__(self, api_key):
        """
        Constructor to create a new object. This API uses a Bearer token
        for authorization included as an HTTP header named "api_key".
        """

        # Call the base class constructor to pass in the base URL
        super().__init__(base_url="https://investigate.api.umbrella.com")

        # Update the existing headers dictionary with the authz token
        self.headers["Authorization"] = f"Bearer {api_key}"

    def req(self, resource, **kwargs):
        """
        Issues a generic HTTP request to a specific resource using the parent
        base_url() functionality. Any other keyword arguments are
        transparently passed through. Returns the HTTP response body
        as JSON (Python objects) or an empty dicitonary if no body exists.
        """

        # Call the base_req method. Headers have already been updated, so
        # there is nothing additional to pass in
        resp = super().base_req(resource, **kwargs)

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}

    @staticmethod
    def build_from_env_vars():
        """
        Static class-level helper method to quickly create a new CiscoTG
        object using environment variables:
          1. UMB_INV_API_KEY: The API key for the Umbrella Investigate API
        """

        (api_key,) = CiscoEndpointBase.load_env_vars("UMB_INV_API_KEY")
        return CiscoUmbrellaInvestigate(api_key)
