#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco Stealthwatch Enterprise
to simplify API interactions.
"""

import time
from datetime import datetime, timedelta
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

    def get_flows_from_ips(self, last_n_minutes, limit, source_ips):
        """
        Collect all flows from specific IP addresses in a given time period
        and up to a given limit.
        """

        # Compute the current time and N minutes ago time
        now = datetime.utcnow()
        n_min_ago = now - timedelta(minutes=last_n_minutes)

        # Format the strings in the proper format, eg 2020-07-16T12:03:00Z
        start_time = n_min_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"Flow query range: {start_time} to {end_time}")

        # Define HTTP body to start the flow query
        body = {
            "startDateTime": start_time,
            "endDateTime": end_time,
            "recordLimit": limit,
            "subject": {"ipAddresses": {"includes": source_ips}},
            "flow": {"flowDirection": "BOTH", "includeInterfaceData": True},
        }

        # Construct the URL and issue the request, including the body
        flow_url = f"sw-reporting/v2/tenants/{self.tenant_id}/flows/queries"
        flow_resp = self.req(flow_url, method="post", json=body)

        # Extract the query ID and print a status message
        query_id = flow_resp["data"]["query"]["id"]
        print(f"Performing flow query with id {query_id}")

        # Loop forever, waiting 5 seconds in between requests
        while True:
            time.sleep(5)

            # Get the flow status to check for completion, and print message
            status_resp = self.req(f"{flow_url}/{query_id}")
            status_msg = status_resp["data"]["query"]["status"].lower()
            print(f"Status of query {query_id}: {status_msg}")

            # If the flow is complete, break from the loop
            if status_msg == "completed":
                break

        # Flow collection complete; return a list of dicts containing flows
        flows = self.req(f"{flow_url}/{query_id}/results")
        return flows["data"]["flows"]


if __name__ == "__main__":

    # Initiate connection to DevNet sandbox and logout
    swe = CiscoSWEnterprise.devnet_reservable()
    print("Creation of CiscoSWEnterprise successful")

    # Perform logout to release cookie
    swe.logout()
    print("Logout successful")
