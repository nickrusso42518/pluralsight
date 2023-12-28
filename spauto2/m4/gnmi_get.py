#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the GenericgNMI class by collecting bogon routes.
"""

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

    # Use string formatting to construct IPv4/v6 paths
    path_template = (
        "Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/"
        "address-family/vrfipv{0}/vrf-unicast/vrf-prefixes"
    )
    path_v4 = path_template.format("4")
    path_v6 = path_template.format("6")

    # Open a new connection to the XR device by unpacking dict into kwargs
    with GenericgNMI(**xr_conn_params) as conn:

        # Loop over each path string
        for path_str in [path_v4, path_v6]:

            # Send a Get RPC and print the response
            print(f"Sending Get RPC for {path_str}")
            get_resp = conn.get(path_str=path_str)
            print(get_resp)


if __name__ == "__main__":
    main()
