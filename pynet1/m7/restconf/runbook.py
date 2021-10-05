#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using Nornir with IOS-XE RESTCONF API
for infrastructure as code. This is a very modern approach.
"""

import requests
from nornir import InitNornir
from nornir.plugins.tasks.apis import http_method
from nornir.plugins.functions.text import print_result


def manage_rt(task, vrf_target, headers):
    """
    Run 3 tasks in sequence:
      1. HTTP GET to capture VRF config
      2. HTTP PUT to update VRF config based on host vars
      3. HTTP POST to save config
    """

    # Host-specific URL based on the current host
    base_url = f"https://{task.host.hostname}/restconf/"

    # TASK 1: Use http_method to get the VRF config via HTTP GET
    task.run(
        task=http_method,
        name="Get VRF config via HTTP GET",
        method="get",
        url=base_url + vrf_target,
        auth=("pyuser", "pypass"),
        headers=headers["get"],
        verify=False,
    )

    # TASK 2: Use http_method to update the VRF config via HTTP PUT
    task.run(
        task=http_method,
        name="Update VRF config via HTTP PUT",
        method="put",
        url=base_url + vrf_target,
        auth=("pyuser", "pypass"),
        headers=headers["put_post"],
        verify=False,
        json=task.host["body"],
    )

    # TASK 3: Use http_method to save the VRF config via HTTP POST
    task.run(
        task=http_method,
        name="Save VRF config via HTTP POST",
        method="post",
        url=base_url + "operations/cisco-ia:save-config",
        auth=("pyuser", "pypass"),
        headers=headers["put_post"],
        verify=False,
    )


def main():
    """
    Execution begins here.
    """

    # Disable SSL warnings in a test environment
    # This is the only reason we had to import "requests"
    requests.packages.urllib3.disable_warnings()

    # Define URL strings and HTTP header dicts ahead of time.
    # This simplifies the readability and flow of nornir task invocations
    vrf_target = "data/Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:vrf"
    headers = {
        "get": {"Accept": "application/yang-data+json"},
        "put_post": {
            "Content-Type": "application/yang-data+json",
            "Accept": "application/yang-data+json, application/yang-data.errors+json",
        },
    }

    # Initialize nornir and invoke the grouped task. This task
    # is limited to IOS-XE devices only, but in the future, you
    # can remove the filter to include IOS-XR (and other groups), too.
    nornir = InitNornir()
    ios_only = nornir.filter(platform="ios")
    result = ios_only.run(
        task=manage_rt,
        name="Manage devices via RESTCONF",
        vrf_target=vrf_target,
        headers=headers,
    )

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken. Standard Python logging
    # levels are supported to set output verbosity.
    print_result(result)


if __name__ == "__main__":
    main()
