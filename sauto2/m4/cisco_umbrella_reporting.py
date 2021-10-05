#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around the Cisco Umbrella Reporting API
to simplify API interactions.
"""

from cisco_endpoint_base import CiscoEndpointBase


class CiscoUmbrellaReporting(CiscoEndpointBase):
    """
    Declaration of Cisco Umbrella Reporting SDK class.
    """

    def __init__(self, api_key, api_secret, org_id):
        """
        Constructor to create a new object. Umbrella Reporting uses HTTP basic
        auth so the constructor requires a api_key and api_secret. Also takes
        in the numeric organization ID for your Umbrella account.
        """

        # Call the base class constructor to pass in the base URL
        base_url = f"https://reports.api.umbrella.com/v1/organizations/{org_id}"
        super().__init__(base_url=base_url)

        # Store the HTTP basic auth parameters in a 2-tuple for use later
        self.auth = (api_key, api_secret)

    def req(self, resource, **kwargs):
        """
        Issues a generic HTTP to the specific resource using the parent
        base_url() functionality. Any other keyword arguments are
        transparently passed through. Returns the HTTP response body
        as JSON (Python objects) or an empty dicitonary if no body exists.
        """

        # Call the base_req method and include the HTTP basic auth tuple
        resp = super().base_req(resource, auth=self.auth, **kwargs)

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}

    @staticmethod
    def build_from_env_vars():
        """
        Static class-level helper method to quickly create a new
        CiscoUmbrellaReporting object using environment variables:
          1. UMB_REP_API_KEY: Your personal API key (username)
          2. UMB_REP_API_SECRET: Your personal API secret (password)
          3. UMB_REP_ORG_ID: Numeric organization ID assigned to you
        """

        api_key, api_secret, org_id = CiscoEndpointBase.load_env_vars(
            "UMB_REP_API_KEY", "UMB_REP_API_SECRET", "UMB_REP_ORG_ID"
        )
        return CiscoUmbrellaReporting(api_key, api_secret, org_id)
