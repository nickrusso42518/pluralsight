#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco Stealthwatch Cloud
to simplify API interactions.
"""

import os
from cisco_sw_base import CiscoSWBase


class CiscoSWCloud(CiscoSWBase):
    """
    Declaration of Cisco Stealthwatch Cloud (SWC) SDK class.
    """

    def __init__(self, account_name, email, api_key):
        """
        Constructor to create a new object. SWC uses a custom
        Authorization header (similar to HTTP basic auth) with the
        user's email address and API key
        """

        # Retain the base URL and create a new, long-lived HTTP session
        host = f"{account_name}.obsrvbl.com"
        super().__init__(host=host)

        # Create the base URL which is used for all requests
        self.base_url = f"https://{self.host}/api/v3"

        # Update the headers dictionary with the authorization header
        self.headers["Authorization"] = f"ApiKey {email}:{api_key}"

    @staticmethod
    def build_from_env_vars():
        """
        Static class-level helper method to quickly create a new
        CiscoSWCloud object using environment variables:
          1. SWC_ACCOUNT: your Stealthwatch Cloud URL identifier
          2. SWC_EMAIL: your Stealthwatch Cloud registered email
          3. SWC_API_KEY: your Stealthwatch Cloud hexadecimal API key
        """

        # Trivial, copy/paste approach to load variables
        # For a more dynamic approach, see "endpoint security" course
        account_name = os.environ.get("SWC_ACCOUNT")
        if not account_name:
            raise ValueError("Env var SWC_ACCOUNT not specified")

        email = os.environ.get("SWC_EMAIL")
        if not email:
            raise ValueError("Env var SWC_EMAIL not specified")

        api_key = os.environ.get("SWC_API_KEY")
        if not api_key:
            raise ValueError("Env var SWC_API_KEY not specified")

        # Return new SWC object based on these env vars
        return CiscoSWCloud(account_name, email, api_key)
