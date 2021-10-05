#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Python client SDK for Cisco FMC.
Check out the API explorer at "https://<fmc_host>/api/api-explorer"
"""

import os
import json
import requests


# Maps the type of an object to the API resource string
URL_MAP = {
    "Host": "object/hosts",
    "Network": "object/networks",
    "NetworkGroup": "object/networkgroups",
    "ProtocolPortObject": "object/protocolportobjects",
    "PortObjectGroup": "object/portobjectgroups",
}


class CiscoFMC:
    """
    Python client SDK for Cisco FMC.
    """

    def __init__(
        self,
        username,
        password,
        host="fmcrestapisandbox.cisco.com",
        verify=False,
    ):
        """
        Constructor for the class. Takes in optional hostname/IP, username,
        password, and optional SSL verification setting. If left blank,
        the reservable DevNet sandbox will be used by default for the host.
        but the username/password change for each reservation.
        """

        # Store all input parameters and assemble the base URL
        self.username = username
        self.password = password
        self.verify = verify
        self.base_url = f"https://{host}/api"

        # If we aren't verifying SSL certificates, disable obnoxious warnings
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a stateful HTTPS session to improve performance
        self.sess = requests.session()

        # Perform initial authentication, which also generates the API path
        # and reusable HTTP header dictionary
        self.authenticate("generatetoken")

    #
    # General management methods/utilities
    #

    @staticmethod
    def build_from_env_vars():
        """
        Static class-level helper method to quickly create a new CiscoFMC
        object using environment variables:
          1. FMC_USERNAME: Your personal username for FMC
          2. FMC_PASSWORD: Your personal password for FMC
        """

        # Collect username and password (required) from env vars
        username = os.environ.get("FMC_USERNAME")
        if not username:
            raise ValueError("Must define FMC_USERNAME environment var")

        password = os.environ.get("FMC_PASSWORD")
        if not password:
            raise ValueError("Must define FMC_PASSWORD environment var")

        # Specifying the host is optional; defaults to DevNet sandbox
        host = os.environ.get("FMC_HOST", "fmcrestapisandbox.cisco.com")

        # Create and return new CiscoFMC object
        return CiscoFMC(username=username, password=password, host=host)

    def authenticate(self, grant_type):
        """
        Perform authentication, either "generatetoken" or "refreshtoken",
        and retain the new tokens as attributes of the object.
        """

        # Construct the proper auth URL based on the grant type. Notice that
        # this URL uses "fmc_platform" vs the more common "fmc_config"
        auth_url = f"{self.base_url}/fmc_platform/v1/auth/{grant_type}"

        # Issue the POST request using either basic auth or the API token.
        # Be sure to ignore SSL cert checking in the FMC sandbox.
        if grant_type == "generatetoken":
            token_resp = self.sess.post(
                auth_url,
                auth=(self.username, self.password),
                verify=self.verify,
            )
        elif grant_type == "refreshtoken":
            token_resp = self.sess.post(
                auth_url, headers=self.headers, verify=self.verify
            )
        token_resp.raise_for_status()

        # Create the common headers from this point forward; technically
        # the refresh token isn't necessary for non-refresh calls, but
        # easier to store it here than in a separate attribute
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-access-token": token_resp.headers["X-auth-access-token"],
            "X-auth-refresh-token": token_resp.headers["X-auth-refresh-token"],
        }

        # Next, define the base URL, which includes the common domain ID.
        # You can access this using the "global" or "DOMAIN_UUID" key.
        # This is part of the URL for many requests in the future
        domain_id = token_resp.headers["global"]
        self.api_path = f"{self.base_url}/fmc_config/v1/domain/{domain_id}"

    def reauthenticate(self):
        """
        Uses the 'refresh_token' to reauthenticate the session to FMC.
        """
        self.authenticate("refreshtoken")

    def req(self, resource, method="get", **kwargs):
        """
        Execute an arbitrary HTTP request by supplying a resource without
        a leading slash to be appended to the base URL. Any other keyword
        arguments supported by 'requests.request' are supported here,
        such as data, json, files, params, etc.
        """

        # Issue the general request based on method arguments
        resp = self.sess.request(
            url=f"{self.api_path}/{resource}",
            method=method,
            headers=self.headers,
            verify=self.verify,
            **kwargs,
        )

        # Optional debugging to view the response body if it exists
        # if resp.text:
        #    print(json.dumps(resp.json(), indent=2))

        # Ensure the request succeeded
        resp.raise_for_status()

        # If body exists, turn to JSON and return; Else, return empty dict
        if resp.text:
            return resp.json()

        return {}

    def _clean(self, obj):
        """
        FMC often requires stripped down object dictionaries to only include
        the name, type, and id keys. Additional keys may cause requests to fail.
        Returns a new dictionary that copies only these three kv pairs.
        """
        return {"name": obj["name"], "type": obj["type"], "id": obj["id"]}

    #
    # Policy object management
    #

    def add_object(self, obj_body):
        """
        Creates a new generic policy object given a complete object body.
        """

        # Issue a POST request, print a status message, and return response
        obj_url = URL_MAP[obj_body["type"]]
        resp = self.req(obj_url, method="post", json=obj_body)
        print(f"Added {resp['type']} named {resp['name']} with ID {resp['id']}")
        return resp

    def add_group(self, group_dict):
        """
        Given a complete object group, create all objects in the group and
        the group itself, along with all proper group memberships.
        """

        # Cannot create empty groups, so build objects individually first
        for obj_body in group_dict["objects"]:
            obj_resp = self.add_object(obj_body)

            # Add a new "id" key with the ID returned and
            # remove "value" key if it exists (it always should)
            obj_body["id"] = obj_resp["id"]
            obj_body.pop("value", None)

        # All objects built; update the group's "objects" key
        group_resp = self.add_object(group_dict)

        # Return the group response which will contain all UUIDs
        return group_resp

    def add_group_file(self, filename):
        """
        Simplifies adding new object groups by reading in the HTTP body
        from JSON files. See "add_group" for logic.
        """
        with open(filename, "r") as handle:
            group_dict = json.load(handle)
        return self.add_group(group_dict)

    def purge_group_id(self, group_id, group_type):
        """
        Deletes an existing object group and all of its contained objects
        for cleanup purposes. Requires the group ID and type as
        specified in the initial response when the group was created
        or collected.
        """

        # Get the proper URL for the group based on type, then collect the
        # group to get the list of objects inside
        group_url = URL_MAP[group_type]
        group = self.req(f"{group_url}/{group_id}")

        # Delete the group first and print a status message
        self.req(f"{group_url}/{group_id}", method="delete")
        print(f"Deleted {group_type} named {group['name']} with ID {group_id}")

        # Iterate over each object, find the proper URL, and delete the object
        for obj in group["objects"]:
            obj_url = URL_MAP[obj["type"]]
            self.req(f"{obj_url}/{obj['id']}", method="delete")
            print(
                f"Deleted {obj['type']} named {obj['name']} with ID {obj['id']}"
            )


def main():
    """
    Quickly test the FMC class authentication capabilities.
    """

    # Create a new FMC object, which performs initial auth; show the tokens
    fmc = CiscoFMC.build_from_env_vars()
    print(fmc.headers["X-auth-access-token"])
    print(fmc.headers["X-auth-refresh-token"])

    # Reauthenticate using the refresh token; show the tokens
    fmc.reauthenticate()
    print(fmc.headers["X-auth-access-token"])
    print(fmc.headers["X-auth-refresh-token"])


if __name__ == "__main__":
    main()
