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

    # Load the generic variables for all devices outside of the loop
    with open("vars/inputs.yml", "r") as handle:
        data = safe_load(handle)

    # Setup the jinja2 templating environment and render the template
    j2_env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = j2_env.get_template("templates/routing.j2")
    new_config = template.render(data=data)

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
