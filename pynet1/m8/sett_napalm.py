#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using NAPALM via SSH to interact with multiple
platforms to collect structured data.
"""

from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load
from parse_rt_m8 import get_rt_parser, rt_diff


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
        device = driver(
            hostname=host["name"], username="pyuser", password="pypass"
        )

        # Open the connection and get the model ID
        print("Opening device and fathering facts")
        device.open()
        facts = device.get_facts()
        print(f"{host['name']} model type: {facts['model']}")

        # Determine the parser, run the proper show command, and perform parsing
        # NAPALM has open issue to obviate need for parser:
        # https://github.com/napalm-automation/napalm/issues/502
        output = device.cli([host["vrf_cmd"]])
        parse_rt = get_rt_parser(host["platform"])
        vrf_data = parse_rt(output[host["vrf_cmd"]])

        # Read the YAML file into structured data, may raise YAMLError
        with open(f"vars/{host['name']}_vrfs.yml", "r") as handle:
            vrfs = safe_load(handle)

        # Find the difference in RTs between intended and actual configs
        rt_updates = rt_diff(vrfs["vrfs"], vrf_data)

        # Template the configuration changes based on the RT updates
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(
            f"templates/sett/{host['platform']}_vpn.j2"
        )
        new_vrf_config = template.render(data=rt_updates)

        # Use NAPALM built-in merging to compare and merge RT updates
        device.load_merge_candidate(config=new_vrf_config)
        diff = device.compare_config()
        if diff:
            print(diff)
            print("Committing configuration changes")
            device.commit_config()
        else:
            print("no diff; config up to date")

        # All done; close the connection
        device.close()
        print("OK!\n")


if __name__ == "__main__":
    main()
