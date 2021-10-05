#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Python client SDK for Cisco FTD.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import json
import requests


# Maps the type of an object to the API resource string
URL_MAP = {
    "networkobject": "object/networks",
    "networkobjectgroup": "object/networkgroups",
    "tcpportobject": "object/tcpports",
    "udpportobject": "object/udpports",
    "protocolobject": "object/protocols",
    "portobjectgroup": "object/portgroups",
}


class CiscoFTD:
    """
    Python client SDK for Cisco FTD.
    """

    def __init__(
        self,
        host="10.10.20.65",
        username="admin",
        password="Cisco1234",
        verify=False,
    ):
        """
        Constructor for the class. Takes in optional hostname/IP, username,
        password, and optional SSL verification setting. If left blank,
        the reservable DevNet sandbox will be used by default.
        """

        # Store all input parameters and assemble the base URL
        self.username = username
        self.password = password
        self.verify = verify
        self.api_path = f"https://{host}/api/fdm/latest"

        # If we aren't verifying SSL certificates, disable obnoxious warnings
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a stateful HTTPS session to improve performance
        self.sess = requests.session()

        # To authenticate, we issue a POST request with our username/password
        # as a JSON body to obtain a bearer token in response. These headers
        # are reusable because almost all API interactions use JSON
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Perform initial authentication
        self.authenticate("password")

    #
    # General management methods/utilities
    #

    def authenticate(self, grant_type):
        """
        Perform authentication, either initial or refresh, and retain the new
        tokens as attributes of the object.
        """

        # This is the JSON payload included in the initial POST request to
        # obtain a bearer token.
        token_data = {"grant_type": grant_type}
        if grant_type == "refresh_token":
            token_data["refresh_token"] = self.refresh_token
        elif grant_type == "password":
            token_data.update(
                {"username": self.username, "password": self.password}
            )

        # Issue the POST request to the proper URL with the predefined headers
        # and body dictionaries. Be sure to ignore SSL cert checking as this
        # is a standalone sandbox FTD instance.
        token_resp = self.sess.post(
            f"{self.api_path}/fdm/token",
            headers=self.headers,
            json=token_data,
            verify=self.verify,
        )
        token_resp.raise_for_status()

        # We've obtained the token data; extract the critical values
        token_data = token_resp.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]

        # Update the headers dictionary with the new access token
        self.headers["Authorization"] = f"Bearer {self.access_token}"

    def reauthenticate(self):
        """
        Uses the 'refresh_token' to reauthenticate the session to FTD.
        """
        self.authenticate("refresh_token")

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
        #     print(json.dumps(resp.json(), indent=2))

        # Ensure the request succeeded
        resp.raise_for_status()

        # If body exists, turn to JSON and return; Else, return empty dict
        if resp.text:
            return resp.json()

        return {}

    #
    # Policy object management
    #

    def add_object(self, obj_body):
        """
        Creates a new generic policy object given a complete object body.
        """

        # Get the proper resource URL given the obj_body type
        resource = URL_MAP[obj_body["type"]]

        # Issue a POST request, print a status message, and return response
        resp = self.req(resource, method="post", json=obj_body)
        print(f"Added {resp['type']} named {resp['name']} with ID {resp['id']}")
        return resp

    def add_group(self, group_dict):
        """
        Given a complete object group, create all objects in the group and
        the group itself, along with all proper group memberships.
        """

        # Cannot create empty groups, so build objects individually first
        created_objects = []
        for obj_body in group_dict["objects"]:
            obj_resp = self.add_object(obj_body)

            # Add the response to a list to replace the group "objects"
            created_objects.append(obj_resp)

        # All objects built; update the group's "objects" key
        group_dict["objects"] = created_objects
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

    def purge_group_name(self, name, group_type):
        """
        Simplifies purging existing object groups and all their contained
        objects by specifying the group's name. See "purge_group_id"
        for logic.
        """
        group_url = URL_MAP[group_type]
        group = self.req(group_url, params={"filter": f"name:{name}"})

        # Presumably, only one item will be returned (can add more checks)
        if len(group["items"]) == 1:
            group_id = group["items"][0]["id"]
            print(f"Found {group_type} named {name} with ID {group_id}")
            return self.purge_group_id(group_id, group_type)

        return None

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
    Quickly test the FTD class authentication capabilities.
    """

    # Create a new FTD object, which performs initial auth; show the tokens
    ftd = CiscoFTD()
    print("First access token")
    print(ftd.access_token)
    print("First refresh token")
    print(ftd.refresh_token)

    # Reauthenticate using the refresh token; show the tokens
    ftd.reauthenticate()
    print("Second access token")
    print(ftd.access_token)
    print("Second refresh token")
    print(ftd.refresh_token)


if __name__ == "__main__":
    main()
