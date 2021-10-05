#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the command runner tool on
Cisco DNA center via API calls.
"""

import json
import os
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    # Collect the list of switches using query parameters. Specifically,
    # we only want Catalyst 9300s because we know our template will work
    search_params = {
        "family": "Switches and Hubs",
        "type": "Cisco Catalyst 9300 Switch",
    }
    devices = dnac.req("dna/intent/api/v1/network-device", params=search_params)

    # Only connect to valid devices (those without errors)
    device_uuids = []
    for dev in devices.json()["response"]:
        # If errorCode is false-y, that means no error, so add the device
        if not dev["errorCode"]:
            print(f"Adding {dev['hostname']}: {dev['instanceUuid']}")
            device_uuids.append(dev["instanceUuid"])

        # Else an error occurred, so don't add the device (do nothing)
        else:
            print(f"Ignoring {dev['hostname']}: {dev['errorCode']}")

    # Build the HTTP body which tells DNAC which commands to run
    # on which devices (identified by UUID)
    # Size limits at the time of this recording:
    #   'commands' length maximum is 5
    #   'device_uuids' length maximum is 20
    command_body = {
        "commands": ["show inventory", "show version", "show badstuff"],
        "deviceUuids": device_uuids,
    }

    # Issue POST request using the command_body just built
    run_resp = dnac.req(
        "dna/intent/api/v1/network-device-poller/cli/read-request",
        method="post",
        jsonbody=command_body,
    )

    # Wait for async job to complete
    run_task = dnac.wait_for_task(run_resp.json()["response"]["taskId"])

    # Parse the file dictionary from the progress string, and download file
    file_id = json.loads(run_task.json()["response"]["progress"])["fileId"]
    file_resp = dnac.req(f"dna/intent/api/v1/file/{file_id}")

    # Create cmd_outputs directory if it doesn't already exist
    file_dir = "cmd_outputs"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Loop through list of dicts in the file response
    for item in file_resp.json():
        uuid = item["deviceUuid"]

        # Loop over each type of result: SUCCESS, FAILURE, BLACKLISTED
        # along with the command dict inside
        for result, cmd_dict in item["commandResponses"].items():

            # Loop over the command dict of command/output pairs
            for cmd, output in cmd_dict.items():
                print(f"{uuid}: {cmd} -> {result}")

                # Use underscores in filenames instead of spaces (cleaner)
                cmd_u = cmd.replace(" ", "_")
                with open(f"{file_dir}/{uuid}_{cmd_u}.txt", "w") as handle:
                    handle.write(output)


if __name__ == "__main__":
    main()
