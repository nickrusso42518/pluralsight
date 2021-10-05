#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets the current network objects from the FTD sandbox.
This script uses a recursive helper function to support pagination.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import json
import requests
from auth_token import get_token


# Limits how many items can be returned in a single GET request
LIMIT = 3


def main():
    """
    Execution begins here.
    """

    # The FTD sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/firepower/
    api_path = "https://10.10.20.65/api/fdm/latest"
    token = get_token(api_path)

    # To authenticate, we issue a POST request with our username/password
    # as a JSON body to obtain a bearer token in response.
    get_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Issue a GET request to collect a list of network objects configured
    # on FTD. These are the IP subnets, hosts, and FQDNs that might be
    # included in various security access policies.
    item_list = []
    ftd_get_recursive(
        resource=f"{api_path}/object/networks",
        headers=get_headers,
        item_list=item_list,
    )

    # Iterate over the list of networks and print out a few of the
    # most interesting values such as name, ID, and prefix/FQDN value.
    for net in item_list:
        print(f"Name: {net['name']} ({net['description']})")
        print(f"  ID: {net['id']}")
        print(f"  Type / Value: {net['subType']} / {net['value']}")

    # Write data to a JSON file to simplify future deletions
    outfile = "json_state/present_netobjs.json"
    with open(outfile, "w") as handle:
        json.dump(item_list, handle, indent=2)
    print(f"Saved present network objects to {outfile}")


def ftd_get_recursive(resource, headers, item_list):
    """
    Recursive function to update the "item_list" in-place. The "resource"
    can be a regular resource or a "next" link, allowing the function to
    resolve any number of "next" links to assemble the final list of items.
    """

    # Base case: if resource is None, empty list, empty string ... exit
    if not resource:
        print(f"Paging done, items: {len(item_list)}\n")
        return

    # Otherwise, Resource is valid, so process it.
    # The next link is a list of 1 element, so convert to a regular string
    if isinstance(resource, list):
        resource = resource[0]

    # Issue the GET request and check for errors
    print(f"Next: {resource}, items: {len(item_list)}")
    get_resp = requests.get(
        resource, headers=headers, params={"limit": LIMIT}, verify=False
    )
    get_resp.raise_for_status()

    # Add all collection items to the existing list, and recurse
    # using the "next" link. Carry over all other parameters
    body = get_resp.json()
    item_list.extend(body["items"])
    ftd_get_recursive(body["paging"]["next"], headers, item_list)


if __name__ == "__main__":
    main()
