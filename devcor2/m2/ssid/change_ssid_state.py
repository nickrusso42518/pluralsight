#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to enable or
disable a specific wireless SSID by ID number information in
the public Cisco DevNet sandbox.
"""

import sys
from meraki_helpers import req, find_network


def main(argv):
    """
    Execution begins here.
    """

    # Ensure there are exactly 3 arguments for the script name,
    # SSID number, and off/on state
    if len(argv) != 3:
        print(f"usage: python {argv[0]} <ssid#> <0 (off) -OR- 1 (on)>")
        sys.exit(1)

    # Convert inputs away from strings; guarantees they are valid because
    # if type conversion fails, errors are raised and program crashes
    ssid_number = int(argv[1])
    ssid_enable = bool(int(argv[2]))
    print(f"SSID {ssid_number} enable state being set to {ssid_enable}")

    # Find the DevNet network ID within the DevNet organization.
    # These are default arguments when left unspecified
    devnet_network = find_network()

    # Perform an HTTP PUT to update an existing SSID by number by changing
    # the enabled state. HTTP PUT in most REST APIs is idempotent so
    # if the state doesn't change, Meraki won't do anything.
    put_resp = req(
        f"networks/{devnet_network}/ssids/{ssid_number}",
        method="put",
        json={"enabled": ssid_enable},
    )
    put_resp_json = put_resp.json()

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(put_resp_json, indent=2))

    print(f"SSID enabled state is currently {put_resp_json['enabled']}")


if __name__ == "__main__":
    main(sys.argv)
