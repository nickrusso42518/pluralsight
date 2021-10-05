#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to create/update
external captive portal (excap) settings on Meraki SSIDs.
"""

import os
import json
import sys
from meraki_helpers import get_network_id, req


def main(org_name, net_name, file_name):
    """
    Execution begins here.
    """

    # Find the network ID for our reserved instance (or personal org)
    net_id = get_network_id(net_name, org_name)

    # Load in the portal dictionary from the specified file
    with open(file_name, "r") as handle:
        portals = json.load(handle)

    # Loop will only run once, but this allows us to put multiple
    # portals in a single file for future batch processing
    for ssid_number, body in portals.items():

        # Assemble the SSID base URL and the HTTP PUT request payload
        ssid_base = f"networks/{net_id}/ssids/{ssid_number}"

        # Issue the PUT request to update the SSID general parameters
        print(f"Updating SSID {ssid_number} for {body['ssid_body']['name']}")
        update_ssid = req(ssid_base, method="put", jsonbody=body["ssid_body"])

        # Debugging statement to check the updated SSID information
        # print(json.dumps(update_ssid.json(), indent=2))

        # Issue the PUT request to update splash page parameters if they exist
        if body["splash_body"]:
            print(
                f"Update SSID {ssid_number} excap "
                f"to {body['splash_body']['splashUrl']}"
            )
            update_splash = req(
                f"{ssid_base}/splashSettings",
                method="put",
                jsonbody=body["splash_body"],
            )

        # Debugging statement to check the updated splash information
        # print(json.dumps(update_splash.json(), indent=2))


if __name__ == "__main__":
    # Get the org name from the env var; default to DevNet
    org = os.environ.get("MERAKI_ORG_NAME", "DevNet Sandbox")

    # Get the network name from the env var; default to DevNet
    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    # Ensure the user supplied a CLI argument to specify the portals file
    if len(sys.argv) != 2:
        print("usage: python build_portals.py <path_to_json_file>")
        sys.exit(1)

    # Ensure the supplied file exists
    json_file = sys.argv[1]
    if not os.path.exists(json_file):
        print(f"file '{json_file}' does not exist")
        sys.exit(2)

    # Pass in the org and network arguments into main()
    main(org, net, json_file)
