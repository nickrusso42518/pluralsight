#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Test the CiscoXRgRPC telemetry subscription functionality.
"""

import argparse
from cisco_xr_grpc import CiscoXRgRPC, Encode

def main(args):
    """
    Test the CiscoXRgRPC telemetry subscription functionality.
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

        # Collect telemetry responses using argument-specific settings
        encoding = Encode(args.encoding)
        responses = conn.create_subs(args.subname, encode=encoding)
        for response in responses:
            print(response)

if __name__ == "__main__":

    # Define CLI arguments for enccoding and subscription name
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encoding", type=int, default=4)
    parser.add_argument("-s", "--subname", type=str, default="perf")

    # Pass arguments into the main() function for evaluation
    main(parser.parse_args())
