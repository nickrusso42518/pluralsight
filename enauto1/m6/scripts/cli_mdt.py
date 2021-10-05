#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via netmiko to configure MDT subscriptions.
"""

import sys
from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader


def main(hosts):
    """
    Execution starts here.
    """

    # Load the generic subscriptions for all devices
    with open("vars/mdt.yml", "r") as handle:
        data = safe_load(handle)

    # Setup the jinja2 templating environment and render the template
    j2_env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
    )
    template = j2_env.get_template("templates/mdt_cli.j2")
    new_config = template.render(data=data)

    # Optional debugging statement to see the CLI commands
    print(new_config)

    # Iterate over hosts supplied by CLI args
    for host in hosts:

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko(
            host=host,
            username="cisco",
            password="cisco",
            device_type="cisco_ios",
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        # Send the configuration string to the device. Netmiko
        # takes a list of strings, not a giant \n-delimited string,
        # so use the .split() function
        conn.send_config_set(new_config.split("\n"))

        # Netmiko automatically collects the results; you can ignore them
        # or process them further
        print(f"Added ({len(data['subscriptions'])}) subscriptions on {host}")

        conn.disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python cli_mdt.py <host1> ... <hostN>")
        sys.exit(1)

    main(sys.argv[1:])
