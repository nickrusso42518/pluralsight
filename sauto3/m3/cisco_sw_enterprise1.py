#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco Stealthwatch Enterprise
to simplify API interactions.
"""

from cisco_sw_base import CiscoSWBase


class CiscoSWEnterprise(CiscoSWBase):
    """
    Declaration of Cisco Stealthwatch Enterprise (SWE) SDK class.
    """

    def __init__(self, smc_host, username, password, tenant_name, verify=False):
        """
        Constructor to create a new object. SWE uses a username/password
        pair in an HTTP POST body to obtain a cookie, which is automatically
        retained by "requests" when using a session (like SD-WAN).
        """

        # Retain the base URL and create a new, long-lived HTTP session
        super().__init__(host=smc_host, verify=verify)
        self.username = username
        self.password = password

        # Create the base URL, which isn't very generic since SWE has
        # many different API versions and paths
        self.base_url = f"https://{self.host}"

        # Perform initial authentication, ignore response data
        self.refresh_cookie()

        # Collect all tenants; you CANNOT specify an Accept header,
        # even though the response is JSON
        tenants = self.req("sw-reporting/v2/tenants", headers=None)

        # Iterate over all tenants, storing the tenant ID if the
        # tenant exists somewhere in the list of tenants
        for tenant in tenants["data"]:
            if tenant["displayName"].lower() == tenant_name.lower():
                self.tenant_id = tenant["id"]
                break

        # Tenant not found; cannot continue
        else:
            raise ValueError(f"tenant with name {tenant_name} not found")

    def refresh_cookie(self):
        """
        Get an authorization cookie to access the API. This is
        automatically called by the constructor by can be called by
        users manually when cookies expire.
        """

        # Build the key/value body with the username and password for auth
        # This is NOT a JSON body, just web form data
        body = {"username": self.username, "password": self.password}

        # Issue an HTTP POST request with the body above and return response
        resp = self.req("token/v2/authenticate", method="post", data=body)
        return resp

    def logout(self):
        """
        For security reasons, delete the existing cookie to logout.
        """
        self.req("token", method="delete")

    @staticmethod
    def devnet_reservable():
        """
        Class-level method that returns an object referencing the DevNet
        reservable sandbox to make it easier for consumers.
        """
        return CiscoSWEnterprise("10.10.20.60", "admin", "C1sco12345", "abc.inc")


if __name__ == "__main__":

    # Initiate connection to DevNet sandbox and logout
    swe = CiscoSWEnterprise.devnet_reservable()
    print("Creation of CiscoSWEnterprise successful")

    # Perform logout to release cookie
    swe.logout()
    print("Logout successful")
