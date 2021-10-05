#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of the Cisco Digital Network Architecture
(DNA) Center software development kit (SDK) to add a new device
comparable flow to the HTTP POST and async HTTP GET used in the
previous course.
"""

import time
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

    # New device to add, same information as previous course
    new_device_dict = {
        "ipAddress": ["192.0.2.1"],
        "snmpVersion": "v2",
        "snmpROCommunity": "readonly",
        "snmpRWCommunity": "readwrite",
        "snmpRetry": 1,
        "snmpTimeout": 60,
        "cliTransport": "ssh",
        "userName": "nick",
        "password": "secret123!",
        "enablePassword": "secret456!",
    }

    # Unpack the new device dictionary into keyword arguments (kwargs) and
    # pass into the SDK. This also performs data validation, so if we
    # have the wrong data or miss a required field, it tells us.
    add_data = dnac.devices.add_device(**new_device_dict)

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(add_data, indent=2))

    # Wait 10 seconds and get the async task ID
    time.sleep(10)
    task = add_data["response"]["taskId"]
    task_data = dnac.task.get_task_by_id(task)

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(task_data, indent=2))

    # Ensure async task completed successfully
    if not task_data["response"]["isError"]:
        print("New device successfully added")
    else:
        print(f"Async task error seen: {task_data['progress']}")


if __name__ == "__main__":
    main()
