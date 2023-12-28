#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the CiscoXRgRPC class by collecting bogon routes.
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

        static_path = {"Cisco-IOS-XR-ip-static-cfg:router-static": [None]}
        response = conn.get_config(yangpathjson_dict=static_path)

        # Response is a list of dictionaries (based on ConfigGetReply objects)
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
