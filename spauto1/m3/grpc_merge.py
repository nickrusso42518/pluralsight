#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the CiscoXRgRPC class by managing bogon routes.
"""

import json
from cisco_xr_grpc import CiscoXRgRPC

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

    # Open a new connection to the XR device by unpacking dict into kwargs
    with CiscoXRgRPC(**xr_conn_params) as conn:

        # Load the bogons from disk
        with open("inputs/bogons.json", "r") as handle:
            bogons = json.load(handle)

        # Merge the bogons into the existing static routes, report any errors
        response = conn.merge_config(yangjson_dict=bogons)
        print(f"Errors: {response.errors if response.errors else 'N/A'}")


if __name__ == "__main__":
    main()
