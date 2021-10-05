#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco SD-WAN to simplify
API interactions.
"""

import time
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

    def _wait_for_device_action_done(self, uuid, interval=20):
        """
        Some requests are asynchronous and the resources created by
        them need to be required until complete. Continue to
        query for a given UUID until complete, then return the result
        from the final GET request.
        """

        # Other examples used a "for" loop with fixed timeout; this
        # example waits forever until the status changes from "in_progress"
        while True:
            time.sleep(interval)
            check = self._req(f"dataservice/device/action/status/{uuid}")
            if check.json()["summary"]["status"].lower() != "in_progress":
                break
        return check

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

    #
    # Policy template management
    #

    def get_feature_templates(self):
        """
        Collect all feature templates configured on vManage.
        """
        return self._req("dataservice/template/feature")

    def add_fd_vsmart_device_template(self):
        """
        Combine the required factory default feature templates into
        a vSmart template. this includes AAA, security, system, OMP,
        VPN 0, and VPN 512.
        """

        # Collect all feature templates first
        all_temps = self.get_feature_templates()

        # Iterate over all templates
        fd_temps = []
        for temp in all_temps.json()["data"]:

            # If the template is a factory default template
            # and ends with vedge, or is generic AAA, add it
            # to fd_temps by recording the template ID and type
            temp_type = temp["templateType"].lower()
            if temp["factoryDefault"] and (
                temp_type.endswith("vsmart") or temp_type == "aaa"
            ):
                fd_temps.append(
                    {
                        "templateId": temp["templateId"],
                        "templateType": temp["templateType"],
                    }
                )

        # Assemble the POST request body
        body = {
            "templateName": "Basic_template",
            "templateDescription": "Collection of default templates",
            "deviceType": "vsmart",
            "configType": "template",
            "factoryDefault": False,
            "policyId": "",
            "featureTemplateUidRange": [],
            "generalTemplates": fd_temps,
        }

        # Issue the POST request and return the result
        return self._req(
            "dataservice/template/device/feature", method="post", jsonbody=body
        )

    def attach_vsmart_device_template(self, template_id, var_map):
        """
        Given an existing template and supplied variables, attaches
        the vSmart template to all discovered vSmart instances.
        The var_map uses hostnames as keys and a 2-tuple as the value,
        containing the site ID and default gateway IP address as strings:
          var_map = {"vsmart-01": ("100", "10.10.20.254")}
        """

        # Collect all the vSmart devices
        vsmarts = self.get_all_devices(model="vsmart")
        templates = []

        # Iterate over collected vSmarts
        for dev in vsmarts.json()["data"]:

            # Unpack the var_map and assemble the vSmart dict
            site_id, def_gway = var_map[dev["host-name"]]
            vsmart_dict = {
                "csv-status": "complete",
                "csv-deviceId": dev["uuid"],
                "csv-deviceIP": dev["system-ip"],
                "csv-host-name": dev["host-name"],
                "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/address": def_gway,
                "//system/host-name": dev["host-name"],
                "//system/system-ip": dev["system-ip"],
                "//system/site-id": site_id,
                "csv-templateId": template_id,
            }
            templates.append(vsmart_dict)

        # Assemble the POST request body, including a list of each
        # vsmart_dict collected above
        body = {
            "deviceTemplateList": [
                {
                    "templateId": template_id,
                    "device": templates,
                    "isEdited": False,
                    "isMasterEdited": False,
                }
            ]
        }

        # Issue the POST request
        attach_resp = self._req(
            "dataservice/template/device/config/attachfeature",
            method="post",
            jsonbody=body,
        )

        # Extract the attachment action ID and wait for completion
        attach_id = attach_resp.json()["id"]
        return self._wait_for_device_action_done(attach_id)
