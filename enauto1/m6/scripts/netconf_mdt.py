#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using NETCONF via ncclient to configure MDT subscriptions.
"""


import sys
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from ncclient import manager


def main(hosts):
    """
    Execution begins here.
    """

    # Load the generic subscriptions for all devices
    with open("vars/mdt.yml", "r") as handle:
        data = safe_load(handle)

    # Setup the jinja2 templating environment and render the template
    j2_env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
    )
    template = j2_env.get_template("templates/mdt_xml.j2")
    new_config = template.render(data=data)

    # Optional debugging statement to see the XML body
    # print(new_config)

    # Iterate over hosts supplied by CLI args
    for host in hosts:

        # Dictionary containing keyword arguments (kwargs) for connecting
        # via NETCONF. Because SSH is the underlying transport, there are
        # several minor options to set up.
        connect_params = {
            "host": host,
            "username": "cisco",
            "password": "cisco",
            "hostkey_verify": False,
            "allow_agent": False,
            "look_for_keys": False,
            "device_params": {"name": "csr"},
        }

        # Unpack the connect_params dict and use them to connect inside
        # of a "with" context manager. The variable "conn" represents the
        # NETCONF connection to the device.
        with manager.connect(**connect_params) as conn:
            print(f"NETCONF session connected: {host}")

            # Perform the update, and if success, print a message
            config_resp = conn.edit_config(target="running", config=new_config)
            if config_resp.ok:
                print(f"Added ({len(data['subscriptions'])}) subscriptions")

        print(f"NETCONF session disconnected: {host}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python netconf_mdt.py <host1> ... <hostN>")
        sys.exit(1)

    main(sys.argv[1:])
