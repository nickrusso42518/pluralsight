#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect wireless SSID
information in the reservable Cisco DevNet sandbox.
"""

import os
import requests


def find_id_by_name(list_of_dicts, search_name):
    """
    Performs a simple linear search on the supplied list of dictionaries,
    checking the "name" value of each item for a match against search_name.
    Returns the "id" value if an item is found, None otherwise.
    """
    found_id = None
    for item in list_of_dicts:
        if item["name"].lower() == search_name.lower():
            found_id = item["id"]
            break
    return found_id


def get_network_id(net_name, org_name="devnet sandbox"):
    """
    Most configuration changes require specifying the network ID
    being modified, so it is useful to quickly find a given ID
    in the DevNet sandbox (by default) or a custom organization.
    """

    # First, get all organizations
    orgs = req("organizations").json()

    # See if supplied org_name is already present by looping
    # over all collected organizations
    org_id = find_id_by_name(orgs, org_name)

    # If we didn't find the organization
    if not org_id:
        raise ValueError(f"Could not find {org_name} organization")

    # Second, get all networks inside that organization
    nets = req(f"organizations/{org_id}/networks").json()

    # See if supplied net_name is already present by looping
    # over all collected organization networks
    net_id = find_id_by_name(nets, net_name)

    # If we didn't find the network
    if not net_id:
        raise ValueError(f"Could not find {net_name} network")

    # Network ID was found, return it
    return net_id


def req(resource, method="get", jsonbody=None, params=None):
    """
    Helper function to reduce repetitive HTTP requests. Takes in a
    specific REST resource and returns HTTP Response object.
    More generic than previous version, can override "method" although
    GET is the default.
    """

    # Basic variables to reduce typing later. Since Meraki is cloud-based,
    # we target the main Meraki site rather than a dedicated resource. Our
    # API key identifies who we are. Be sure to check the details here:
    # https://developer.cisco.com/meraki/
    api_path = "https://dashboard.meraki.com/api/v0"
    api_key = os.environ.get("MERAKI_API_KEY")
    if not api_key:
        raise ValueError("Must export MERAKI_API_KEY to access API")

    # Define headers. Note that Content-Type isn't needed for GET requests,
    # but it doesn't hurt to statically apply it.
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cisco-Meraki-API-Key": api_key,
    }

    # Assemble the complete URL by appending the resource to the API path,
    # and issue HTTP GET using proper authentication headers
    resp = requests.request(
        method=method,
        url=f"{api_path}/{resource}",
        headers=headers,
        json=jsonbody,
        params=params,
    )

    # If status code >= 400, raise HTTPError
    resp.raise_for_status()

    # HTTP request succeeded; return response object
    return resp
