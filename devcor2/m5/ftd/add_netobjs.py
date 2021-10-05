#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Adds new network objects to the FTD sandbox.
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
    post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Load the new network objects to be added as Python objects
    with open("json_state/new_netobjs.json", "r") as handle:
        network_objs = json.load(handle)

    # Loop over network objects and issue a POST request for each
    # network object to add. Raise HTTPError if anything fails
    for net in network_objs:
        post_resp = requests.post(
            f"{api_path}/object/networks",
            headers=post_headers,
            json=net,
            verify=False,
        )

        # Print object details if success or error fails if failed. We
        # don't wait to raise_for_status() which halts the entire process
        # even if a single element fails
        if post_resp.ok:
            net_json = post_resp.json()
            print(f"Added {net_json['name']} network object at {net_json['id']}")
        else:
            print(f"Couldn't add {net['name']} network object")
            print(f"  Details: {post_resp.status_code} / {post_resp.reason}")


if __name__ == "__main__":
    main()
