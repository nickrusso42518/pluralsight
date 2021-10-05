#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect wireless SSID
information in the reservable Cisco DevNet sandbox.
"""

import requests


def find_network(org_str="devnet", net_str="devnet"):
    """
    Returns the network ID based on the search parameters.
    "org_str" represents a subset of the organization name.
    "net_str" represents a subset of the network name.
    Both strings are case-insensitive and both
    parameters default to "devnet" if left undefined, which
    will function correctly in the public Meraki sandbox.
    """

    # Get the list of organizations from the sandbox
    orgs = req("organizations").json()

    # Iterate over each org. This loop does double-duty. It prints out each
    # discovered organization, but also performs a linear search for the
    # org ID. If the ID is found, it is stored in the variable above.
    org_id = 0
    for org in orgs:
        if org_str.lower() in org["name"].lower():
            org_id = org["id"]
            break

    # If the org ID has been defined (ie, is not 0 in this context)
    # then we will perform another GET request to collect the proper
    # networks. If the org ID hasn't been defined, then we didn't find it
    # so don't try to dig deeper into that organization.
    if org_id:
        networks = req(f"organizations/{org_id}/networks").json()

        # Print each network discovered and search for the specific one.
        # Once found, stored that network ID for later.
        for network in networks:
            if net_str in network["name"].lower():
                return network["id"]

    # Either the organization ID or network wasn't found, return None
    return None


def req(resource, method="get", json=None):
    """
    Helper function to reduce repetitive HTTP requests. Takes in a
    specific REST resource and returns HTTP Response object.
    More generic than previous version, can override "method" although
    GET is the default.
    """

    # Basic variables to reduce typing later. Since Meraki is cloud-based,
    # we target the main Meraki site rather than a dedicated resource. Our
    # API key identifies who we are (in this case, an exploratory read-only
    # user in the DevNet sandbox. The API key is provided by DevNet
    # in the sandbox, but may change over time. Be sure to check here:
    # https://developer.cisco.com/meraki/
    api_path = "https://dashboard.meraki.com/api/v0"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0",
    }

    # Assemble the complete URL by appending the resource to the API path,
    # and issue HTTP GET using proper authentication headers
    resp = requests.request(
        method=method, url=f"{api_path}/{resource}", headers=headers, json=json
    )

    # If status code >= 400, raise HTTPError
    resp.raise_for_status()

    # HTTP request succeeded; return response object
    return resp
