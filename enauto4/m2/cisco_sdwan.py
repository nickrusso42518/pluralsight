#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco SD-WAN to simplify
API interactions.
"""

import json
import requests


class CiscoSDWAN:
    """
    A simple Cisco SD-WAN SDK to demonstrate API interaction.
    """

    def __init__(self, host, port, username, password, verify=False):
        """
        Constructor that creates the long-lived HTTP session and
        performs the initial login.
        """

        # Create the base URL and login credentials needed to authenticate
        self.base_url = f"https://{host}:{port}"

        # Store the verification setting; if false, disable SSL warnings
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a new, long-lived TCP session, and authenticate
        self.session = requests.session()
        auth_resp = self.session.post(
            f"{self.base_url}/j_security_check",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"j_username": username, "j_password": password},
            verify=self.verify,
        )

        # URL almost always returns 200, even upon failure. If any
        # body text is present, that is a failure, likely a credentials issue
        if auth_resp.text:
            auth_resp.status_code = 401
            auth_resp.reason = "UNAUTHORIZED; check username/password"
            auth_resp.raise_for_status()

        # Auth success; define generic headers for all future requests
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    #
    # Class-level methods
    #

    @staticmethod
    def run_api_calls(api_calls, filepath="data_ref"):
        """
        Helper function to iterate over a list of API
        calls and run them. Only works when there are no
        arguments being passed into each API wrapper call
        (mostly for getters).
        """
        for api_call in api_calls:
            resp = api_call()
            name = api_call.__name__
            print(f"Executing '{name}' API call")
            with open(f"{filepath}/{name}.json", "w") as handle:
                json.dump(resp.json(), handle, indent=2)

    @staticmethod
    def get_instance_always_on():
        """
        Factory-style function that retusn a new CiscoSDWAN object
        connected to the DevNet SDWAN Always-On sandbox.
        """
        return CiscoSDWAN(
            host="sandboxsdwan.cisco.com",
            port=8443,
            username="devnetuser",
            password="Cisco123!",
        )

    @staticmethod
    def get_instance_reserved():
        """
        Factory-style function that retusn a new CiscoSDWAN object
        connected to the DevNet SDWAN Reserved sandbox.
        """
        return CiscoSDWAN(
            host="10.10.20.90", port=8443, username="admin", password="admin"
        )

    #
    # Generic internal helpers
    #

    def _req(self, resource, method="get", params=None, jsonbody=None):
        """
        Internal helper function to issue requests and raise errors
        if the request fails. Returns the entire response object
        on success. The requests library is smart enough to treat "data"
        as "json" if the Content-Type is set to application/json.
        """
        resp = self.session.request(
            method=method,
            url=f"{self.base_url}/{resource}",
            headers=self.headers,
            params=params,
            json=jsonbody,
            verify=self.verify,
        )
        resp.raise_for_status()
        return resp

    #
    # Device Inventory APIs
    #

    def get_all_devices(self, model=None):
        """
        Display all Viptela devices in the overlay network that are
        connected to the vManage NMS.
        """
        params = {"device-model": model} if model else None
        return self._req("dataservice/device", params=params)

    def get_device_controllers(self, model=None):
        """
        Display all available controllers—vBond orchestrators,
        vManage NMS, and vSmart controllers—in the overlay network.
        """
        params = {"model": model} if model else None
        return self._req("dataservice/system/device/controllers", params=params)

    def get_device_vedges(self, model=None):
        """
        Display all available vEdge routers in the overlay network.
        """
        params = {"model": model} if model else None
        return self._req("dataservice/system/device/vedges", params=params)
