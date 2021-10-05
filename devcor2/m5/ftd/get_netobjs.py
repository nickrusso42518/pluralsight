#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets the current network objects from the FTD sandbox.
This script does not support pagination.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import json
import requests
from auth_token import get_token


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
    # on the FTD device. Raise HTTPErrors if the request fails
    get_resp = requests.get(
        f"{api_path}/object/networks", headers=get_headers, verify=False
    )
    get_resp.raise_for_status()

    # Iterate over the list of networks and print out a few of the
    # most interesting values such as name, ID, and prefix/FQDN value.
    get_resp_json = get_resp.json()
    for net in get_resp_json["items"]:
        print(f"Name: {net['name']} ({net['description']})")
        print(f"  ID: {net['id']}")
        print(f"  Type / Value: {net['subType']} / {net['value']}")

    # Write data to a JSON file to simplify future deletions
    outfile = "json_state/present_netobjs.json"
    with open(outfile, "w") as handle:
        json.dump(get_resp_json["items"], handle, indent=2)
    print(f"Saved present network objects to {outfile}")


if __name__ == "__main__":
    main()
