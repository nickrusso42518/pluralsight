#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate NETCONF on IOS-XE and IOS-XR coupled
with Nornir to update VRF route-target configurations.
"""

from nornir import InitNornir
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file
from nc_tasks import netconf_edit_config, netconf_commit, netconf_custom_rpc


def manage_config(task):
    """
    Custom task to wrap complex infra-as-code steps:
      1. Load vars from YAML file
      2. Render jinja2 template to get XML text
      3. Send NETCONF edit_config RPC to perform updates
      4. Save configuration to non-volatile memory
    """

    # Assemble the vars file name based on inv hostname, then load the data
    vars_file = f"vars/{task.host.name}_vrfs.yaml"
    task1_result = task.run(task=load_yaml, file=vars_file)

    # Create local variables to represent the template data and filename
    vrfs = task1_result[0].result
    template = f"{task.host.platform}_vpn.j2"

    # Render the NETCONF XML templates given the host-specific VRF data
    task2_result = task.run(
        task=template_file,
        path="templates",
        template=template,
        data=vrfs["vrfs"],
    )

    # Extract the configuration text from the previous result and use NETCONF
    # edit_config RPC to update the device. Include the target datastore and
    # optional operation, just like in the non-Nornir script
    new_vrf_config = task2_result[0].result
    task3_result = task.run(
        task=netconf_edit_config,
        target=task.host["edit_target"],
        config=new_vrf_config,
        default_operation=task.host.get("operation"),
    )

    # Extract the config response and test for success
    config_resp = task3_result[0].result
    if config_resp.ok:

        # Test for IOS-XR, which uses commit RPC to copy from candidate
        # to running config (no concept of startup config)
        if task.host.platform == "iosxr":
            task4_result = task.run(task=netconf_commit)

        # Test for IOS (really IOS-XE), which uses a custom save-config RPC
        # to copy from running config to startup config
        elif task.host.platform == "ios":
            rpc_text = '<save-config xmlns="http://cisco.com/yang/cisco-ia"/>'
            task4_result = task.run(task=netconf_custom_rpc, rpc_text=rpc_text)

        # If the save operation succeeded, print a simple notification msg
        if task4_result[0].result.ok:
            print(f"{task.host.name}: VRFs successfully updated")

    else:
        # The edit_config RPC failed; print the errors for troubleshooting
        print(f"{task.host.name}: Errors: {','.join(config_resp.errors)}")


def main():
    """
    Execution begins here.
    """

    # Initialize Nornir and run the manage_config custom task
    nornir = InitNornir()
    nornir.run(task=manage_config)


if __name__ == "__main__":
    main()
