#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via netmiko to configure network devices.
"""

from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader


def main():
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

        # Load the host-specific VRF declarative state
        with open(f"vars/{host['name']}_vrfs.yml", "r") as handle:
            vrfs = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"templates/netmiko/{platform}_vpn.j2")
        new_vrf_config = template.render(data=vrfs)

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host["name"],
            username="pyuser",
            password="pypass",
            device_type=platform,
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the .split() function
        result = conn.send_config_set(new_vrf_config.split("\n"))

        # Netmiko automatically collects the results; you can ignore them
        # or process them further
        print(result)

        conn.disconnect()


if __name__ == "__main__":
    main()
