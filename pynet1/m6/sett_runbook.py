#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using Nornir to introduce orchestration and
concurrency, as well as inventory management.
"""

import logging
from nornir import InitNornir
from nornir.plugins.tasks.networking import (
    # napalm_cli,
    netmiko_send_command,
    napalm_get,
    napalm_configure,
)
from nornir.plugins.tasks.text import template_file
from nornir.plugins.functions.text import print_result
from parse_rt_m6 import get_rt_parser, rt_diff


def manage_rt(task):
    """
    Grouped task does 4 things:
    1. Gather facts with NAPALM
    2. Gather VRF configuration with Netmiko
    3. Locally render VRF config template
    4. Configure VRF updates with NAPALM
    """

    # TASK 1: Gather facts using NAPALM to get model ID
    task1_result = task.run(task=napalm_get, getters=["get_facts"])
    model = task1_result[0].result["get_facts"]["model"]
    print(f"{task.host.name}: connected as model type {model}")

    # TASK 2: Collect the VRF running configuration using netmiko
    task2_result = task.run(
        task=netmiko_send_command, command_string=task.host["vrf_cmd"]
    )
    cmd_output = task2_result[0].result

    # ALTERNATIVE IMPLEMENTATION: Can use napalm_cli just as easily,
    # but using netmiko and NAPALM together highlights Nornir's flexibility
    # task2_result = task.run(task=napalm_cli, commands=[task.host["vrf_cmd"]])
    # cmd_output = task2_result[0].result[task.host["vrf_cmd"]]

    # Determine the parser and perform parsing.
    parse_rt = get_rt_parser(task.host.platform)
    vrf_data = parse_rt(cmd_output)
    rt_updates = rt_diff(task.host["vrfs"], vrf_data)

    # TASK 3: Create the template of config to add
    task3_result = task.run(
        task=template_file,
        template=f"{task.host.platform}_vpn.j2",
        path="templates/",
        data=rt_updates,
    )
    new_vrf_config = task3_result[0].result

    # TASK 4: Configure the devices using NAPALM and print any updates
    task4_result = task.run(task=napalm_configure, configuration=new_vrf_config)
    if task4_result[0].diff:
        print(f"{task.host.name}: diff below\n{task4_result[0].diff}")
    else:
        print(f"{task.host.name}: no diff; config up to date")


def main():
    """
    Execution begins here.
    """

    # Initialize nornir, nothing new yet.
    nornir = InitNornir()

    # We can run arbitrary Python code, so let's just print the
    # hostnames loaded through the inventory, which are dict keys.
    print("Nornir initialized with inventory hosts:")
    for host in nornir.inventory.hosts.keys():
        print(host)

    # Invoke the grouped task.
    result = nornir.run(task=manage_rt)

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken. Standard Python logging
    # levels are supported to set output verbosity.
    print_result(result, severity_level=logging.WARNING)


if __name__ == "__main__":
    main()
