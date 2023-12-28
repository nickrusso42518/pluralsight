#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the CiscoXRgRPC class by managing bogon routes.
"""

import json
from generic_gnmi import GenericgNMI


def main():
    """
    Execution begin here.
    """

    # Define connectivity information for the XR route server
    xr_conn_params = {
        "host": "10.0.90.41",
        "port": 57777,
        "username": "labadmin",
        "password": "labadmin",
    }

    # Use string formatting to create path template
    path_template = (
        "Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/"
        "address-family/vrfipv{0}/vrf-unicast/vrf-prefixes"
    )

    # Open a new connection to the XR device by unpacking dict into kwargs
    with GenericgNMI(**xr_conn_params) as conn:

        # Loop over each IP version
        for version in ["4", "6"]:

            # Render template by replacing the version ID
            path_str = path_template.format(version)

            # Load version-specific bogons from file
            with open(f"inputs/bogons_v{version}.json", "r") as handle:
                json_data = json.load(handle)

            # Send Set RPC with path and data payload, print reponse
            print(f"Sending Set RPC for {path_str}")
            set_resp = conn.set_update(path_str=path_str, json_data=json_data)
            print(set_resp)


if __name__ == "__main__":
    main()
