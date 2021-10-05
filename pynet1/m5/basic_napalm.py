#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using NAPALM via SSH to interact with multiple
platforms to collect structured data.
"""

from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts from YAML file
    for host in host_root["host_list"]:

        # Determine and create the network driver object based on platform
        print(f"Getting {host['platform']} driver")
        driver = get_network_driver(host["platform"])
        conn = driver(
            hostname=host["name"], username="pyuser", password="pypass"
        )

        # Open the connection and get the model ID
        print("Opening connection and fathering facts")
        conn.open()
        facts = conn.get_facts()
        print(facts)
        print(f"{host['name']} model type: {facts['model']}")

        # Read the YAML file into structured data, may raise YAMLError
        with open(f"vars/{host['name']}_vrfs.yml", "r") as handle:
            vrfs = safe_load(handle)

        # Template the configuration changes based on the RT updates
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(
            f"templates/basic/{host['platform']}_vpn.j2"
        )
        new_vrf_config = template.render(data=vrfs["vrfs"])

        # Use NAPALM built-in merging to compare and merge RT updates
        # Note that dynamically removing configuration is still a challenge
        # unless NAPALM is explicitly told ...
        conn.load_merge_candidate(config=new_vrf_config)
        diff = conn.compare_config()
        if diff:
            print(diff)
            print("Committing configuration changes")
            conn.commit_config()
        else:
            print("no diff; config up to date")

        # All done; close the connection
        conn.close()
        print("OK!\n")


if __name__ == "__main__":
    main()
