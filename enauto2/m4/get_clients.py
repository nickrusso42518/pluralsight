#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect a list
of currently associated clients on a given network.
"""

import os
from meraki_helpers import get_network_id, req


def main(org_name, net_name):
    """
    Execution begins here.
    """

    # Find the network ID for our reserved instance (or personal org)
    net_id = get_network_id(net_name, org_name)

    # Collect the list of clients connected on all SSIDs in this network
    get_clients = req(f"networks/{net_id}/clients").json()

    # Debugging statement to check the updated SSID information
    # import json; print(json.dumps(get_clients, indent=2))

    # Iterate through list of clients, printing each one on
    # a numbered row for easy reviewing
    for i, client in enumerate(get_clients):
        print(
            f"{i+1}. Name: {client['description']}  "
            f"MAC: {client['mac']}  Status: {client['status']}"
        )


if __name__ == "__main__":
    # Get the org name from the env var; default to DevNet
    org = os.environ.get("MERAKI_ORG_NAME", "DevNet Sandbox")

    # Get the network name from the env var; default to DevNet
    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    # Pass in the org and network arguments into main()
    main(org, net)
