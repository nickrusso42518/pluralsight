#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to create/update
networks from a JSON file using the REST API. This may not
work in DevNet sandboxes; try it on a private deployment, too.
"""

import os
import json
from meraki_helpers import find_id_by_name, req


def main(org_name):
    """
    Execution begins here.
    """

    # First, get all organizations
    orgs = req("organizations").json()

    # Print the list of organizations for troubleshooting
    # print(json.dumps(orgs, indent=2))

    # See if supplied org_name is already present by looping
    # over all collected organizations
    org_id = find_id_by_name(orgs, org_name)

    # If we didn't find the organization
    if not org_id:
        raise ValueError("Could not find organization {org_name}")

    # Second, get all networks inside that organization
    print(f"Found {org_name} with ID {org_id}")
    cur_nets = req(f"organizations/{org_id}/networks").json()

    # Print the list of networks for troubleshooting
    # print(json.dumps(cur_nets, indent=2))

    # Load in the networks to add, and iterate over them
    with open("add_networks.json", "r") as handle:
        add_nets = json.load(handle)

    for item in add_nets:

        # See if supplied network name is already present by looping
        # over all collected organization networks
        net_name = item["body"]["name"]
        net_id = find_id_by_name(cur_nets, net_name)

        # The network already exists; not an error, but gracefully exit
        if net_id:
            print(f"Network {net_name} already exists ({net_id})")
            continue

        # Network does not exist, so create it and capture the network ID
        new_net = req(
            f"/organizations/{org_id}/networks",
            method="post",
            jsonbody=item["body"],
        ).json()
        net_id = new_net["id"]
        print(f"Created network {net_name} with ID {net_id}")

        # Debugging statement to display new network configuration
        # print(json.dumps(new_net, indent=2))

        # Iterate over the list of devices that belong in each new network
        # and claim each device individually (no body data returned)
        for device in item["devices"]:
            req(
                f"networks/{net_id}/devices/claim",
                method="post",
                jsonbody=device["add"],
            )
            sn = device["add"]["serial"]
            print(f"Device with SN {sn} added")

            # Although unexpected, the dashboard API does *not* currently allow
            # you to specify the "name" attribute when claiming a device. This
            # must be done afterwards using a PUT request
            update = req(
                f"networks/{net_id}/devices/{sn}",
                method="put",
                jsonbody=device["update"],
            ).json()
            print(f"Device with SN {sn} named {device['update']['name']}")

            # Debugging statement to print the device details after update
            # print(json.dumps(update, indent=2))

            # Sanity check; ensure the name update actually worked
            if update["name"] != device["update"]["name"]:
                raise ValueError("Device name update failed")


if __name__ == "__main__":
    # Get the org name from the env var; default to DevNet
    org = os.environ.get("MERAKI_ORG_NAME", "DevNet Sandbox")

    # Pass in the org name argument into main()
    main(org)
