#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate NETCONF on IOS-XE and IOS-XR coupled
with Nornir to collect and store VRF configuration to disk.
"""

import json
import os
from nornir import InitNornir
from nornir.plugins.tasks.files import write_file
import xmltodict
from nc_tasks import netconf_get_config


def save_config_as_json(task, output_dir):
    """
    Custom task to wrap two simple actions:
      1. NETCONF get_config RPC to collect VRF running configuration
      2. Store JSON data to disk
    """

    # Extract vrf_filter string for each host and issue NETCONF get_config RPC
    vrf_filter = ("subtree", task.host["vrf_filter"])
    result = task.run(task=netconf_get_config, filter=vrf_filter)

    # Create local variables to represent JSON text and target filename
    vrf_dict = xmltodict.parse(result[0].result.xml)
    vrf_json = json.dumps(vrf_dict, indent=2)
    filename = f"{output_dir}/{task.host.name}_running_config.json"

    # Write the JSON text to a local file named after the hostname
    # Don't need to store result; plus, Nornir retains it automatically
    task.run(task=write_file, filename=filename, content=vrf_json)
    print(f"Stored {task.host.name} VRF config in {filename}")


def main():
    """
    Execution begins here.
    """

    # Create specified output directory if it doesn't already exist
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize Nornir and run the save_config_as_json custom task
    nornir = InitNornir()
    nornir.run(task=save_config_as_json, output_dir=output_dir)


if __name__ == "__main__":
    main()
