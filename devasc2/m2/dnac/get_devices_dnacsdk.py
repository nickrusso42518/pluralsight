#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of the Cisco Digital Network Architecture
(DNA) Center software development kit (SDK) to collect a list of
network devices using a comparable flow to the HTTP GET used
in the previous course.
"""

from dnacentersdk import api


def main():
    """
    Execution begins here.
    """

    # Create DNAC object, which automatically handles the token
    # request process. API docs in the link below, which may change:
    # https://dnacentersdk.readthedocs.io/en/latest/api/api.html
    dnac = api.DNACenterAPI(
        base_url="https://sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
    )

    # Use the devices.get_device_list() method to get a list of devices,
    # which is equivalent to the manual HTTP GET in the previous course
    devices = dnac.devices.get_device_list()

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(devices, indent=2))

    # Same exact loop from previous course, just get the device ID
    # and management IP agree printed in a single neat row
    for device in devices["response"]:
        print(f"ID: {device['id']}  IP: {device['managementIpAddress']}")


if __name__ == "__main__":
    main()
