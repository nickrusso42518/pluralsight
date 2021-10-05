#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via netmiko to configure network devices.
"""

from yaml import safe_load
from netmiko import Netmiko


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Load the static configuration snippet
    with open("templates/routing.txt", "r") as handle:
        new_config = handle.read()

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["production"]:

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="cisco",
            password="cisco",
            device_type="cisco_ios",
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the .split() function
        result = conn.send_config_set(new_config.split("\n"))

        # Netmiko automatically collects the results; you can ignore them
        # or process them further
        print(result)

        conn.disconnect()


if __name__ == "__main__":
    main()
