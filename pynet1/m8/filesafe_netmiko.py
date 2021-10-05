#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate SCP file transfer using Netmiko except with
additional file validation. Exits with rc=1 if the wrong number of
command lines arguments are supplied (must be one filename). Exits
with rc=2 if the file supplied does not exist.
"""

import sys
import os
from yaml import safe_load
from netmiko import Netmiko, file_transfer


def main(argv):
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Netmiko uses "cisco_ios" instead of "ios" and
    # "cisco_xr" instead of "iosxr", so use a mapping dict to convert
    platform_map = {"ios": "cisco_ios", "iosxr": "cisco_xr"}

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:

        # Use the map to get the proper Netmiko platform
        platform = platform_map[host["platform"]]

        # Initialize the SSH connection
        print(f"Connecting to {host['name']}")
        conn = Netmiko(
            host=host["name"],
            username="pyuser",
            password="pypass",
            device_type=platform,
        )

        # Upload the file specified. The dict.get(key) function tries
        # to retrieve the value at the specified key and returns None
        # if it does not exist. Very useful in network automation!
        print(f"  Uploading {argv[1]} ... ", end="")
        result = file_transfer(
            conn,
            source_file=argv[1],
            dest_file=argv[1],
            file_system=host.get("file_system"),
        )

        # Print the resulting details
        print("OK!")
        print(f"  Details: {result}")


if __name__ == "__main__":
    # Basic input validation; check CLI args and file existence
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <file_to_upload>")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(f"error: file '{sys.argv[1]}' not found")
        sys.exit(2)

    # At this point, the input has been reasonably checked
    main(sys.argv)
