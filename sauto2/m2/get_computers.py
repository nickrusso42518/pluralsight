#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect the connected computers using the Cisco AMP API.
"""

from cisco_amp import CiscoAMP


def main():
    """
    Execution starts here.
    """

    # Instantiate a new AMP object from env vars and get computer list
    amp = CiscoAMP.build_from_env_vars()
    computers = amp.req("computers")

    # For each computer, print some basic info for verification
    for comp in computers["data"]:
        print(f"Hostname: {comp['hostname']}")
        print(f"OS: {comp['operating_system']}")
        print(f"Last seen: {comp['last_seen']}")
        print(f"GUID: {comp['connector_guid']}\n")


if __name__ == "__main__":
    main()
