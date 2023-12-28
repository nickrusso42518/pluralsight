#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the GenericgNMI class by subscribing to dial-in telemetry.
"""

from generic_gnmi import GenericgNMI, Encoding


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
    with GenericgNMI(**xr_conn_params) as conn:

        path = "Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary"

        # Collect telemetry responses and print them out
        responses = conn.subscribe(path)
        for response in responses:
            print(response)


if __name__ == "__main__":
    main()
