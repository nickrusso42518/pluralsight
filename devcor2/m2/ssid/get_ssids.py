#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect wireless SSID
information in the public Cisco DevNet sandbox.
"""

from meraki_helpers import req, find_network


def main():
    """
    Execution begins here.
    """

    # Find the DevNet network ID within the DevNet organization.
    # These are default arguments when left unspecified
    devnet_network = find_network()

    # Get a list of SSIDs within the DevNet network
    ssids = req(f"networks/{devnet_network}/ssids").json()

    # Debugging line; pretty-print JSON to see structure (list of SSIDs)
    # import json; print(json.dumps(ssids, indent=2))

    # Iterate over the list of SSIDs found, printing their number,
    # enable state, and descriptive name.
    print(f"SSIDs found: {len(ssids)}")
    for ssid in ssids:
        print(f"Num: {ssid['number']:<3} Enabled: {ssid['enabled']:<2}", end="")
        print(f" Name: {ssid['name']}")


if __name__ == "__main__":
    main()
