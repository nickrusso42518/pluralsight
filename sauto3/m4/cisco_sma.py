#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple SDK to abstract Cisco Security Management Appliance
(SMA) requests.
"""

import requests


class CiscoSMA:
    """
    Definition of SMA API wrapper.
    """

    def __init__(
        self,
        host="198.19.10.51",
        port=6443,
        username="admin",
        password="C1sco12345",
        verify=False,
    ):
        """
        Constructor takes in the SMA IP/hostname and HTTP basic
        auth username/password. This method does not issue any requests,
        only initializes data. If no arguments are supplied, method
        uses the Cisco dCloud specifications.
        """

        # Retain supplied host and auth creds, then create a new session
        self.base_url = f"https://{host}:{port}/sma/api/v2.0"
        self.auth = (username, password)
        self.sess = requests.session()

        # If verify is false, we should also disable SSL warnings (sandbox)
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # SMA appears to only use JSON payloads, so hardcode the headers once
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def req(self, resource, method="get", **kwargs):
        """
        Issues a generic HTTP request to a given resource and with given
        keyword arguments. Returns the body of the response, if it exists,
        as Python objects.
        """

        # Sloppy but necessary. "requests" automatically handles URL encoding
        # of special characters, but SMA actually wants the raw ':'
        # Manually assemble the query parameter string instead
        if "params" in kwargs:

            # Manually build the query string in k1=v1&k2=v2 format
            qp_str = "&".join(f"{k}={v}" for k, v in kwargs["params"].items())
            # print(qp_str)

            # Reassign the params dict to the pre-made query params string
            kwargs["params"] = qp_str

        # Issue the generic HTTP request using the object's session attribute
        resp = self.sess.request(
            url=f"{self.base_url}/{resource}",
            method=method,
            auth=self.auth,
            headers=self.headers,
            verify=self.verify,
            **kwargs,
        )

        # If any errors occurred (status code >= 400), raise an HTTPError
        resp.raise_for_status()

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            #import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}


if __name__ == "__main__":

    # Create a new SMA appliance with default (dCloud) parameters
    sma = CiscoSMA()

    # Collect list of SMA-attached appliances
    appliances = sma.req("config/appliances", params={"device_type": "sma"})

    # Loop over list of appliances, then unpack each dictionary item
    for appliance in appliances["data"]["appliances"]:
        for serial_num, attrs in appliance.items():

            # Print the hostname, IP, type, and SN for each appliance
            print(f"Host/IP: {attrs['host_name']}/{attrs['ip_address']}")
            print(f"Type/SN: {attrs['product_type']}/{serial_num}\n")
