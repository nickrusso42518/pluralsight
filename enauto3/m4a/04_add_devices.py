#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Add CLI and SNMPv2 RO/RW credentials to the site
hierarchy to support the SDA fabric.
"""

import json
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    # Can use DevNet reservable instance (10.10.20.85) or dCloud HW sandbox
    # https://dcloud.cisco.com
    dnac = DNACRequester(
        # host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
        host="198.18.129.100",
        username="admin",
        password="C1sco12345",
        verify=False,
    )

    # Load in the JSON data into Python objects
    with open("input_data/devices.json", "r") as handle:
        data = json.load(handle)

    # Issue an HTTP POST request to create the credential
    print("Adding network devices")
    add_resp = dnac.req(
        "dna/intent/api/v1/network-device",
        method="post",
        jsonbody=data,
    )

    # This API uses standard tasks; wait for completion
    dnac.wait_for_task(add_resp.json()["response"]["taskId"])

    # Issue GET to learn ID of building for subpools
    print("Getting site (building) ID")
    params = {"name": "Global/Maryland/secretlab"}
    get_resp = dnac.req("dna/intent/api/v1/site", params=params)
    bld_id = get_resp.json()["response"][0]["id"]

    # Use a list comprehension to build the assignment body
    assign_list = [{"ip": ip} for ip in data["ipAddress"]]
    print(f"Assignments: {json.dumps(assign_list, indent=2)}")

    # Assign credentials to global site using credential dict as body
    print(f"Assigning devices to {bld_id}")
    assign_resp = dnac.req(
        f"dna/system/api/v1/site/{bld_id}/device",
        method="post",
        jsonbody={"device": assign_list},
    )

    # Extract the executionStatusUrl and wait for it to finish being created
    status_url = assign_resp.json()["executionStatusUrl"]
    dnac.wait_for_exec_status(status_url[1:])


if __name__ == "__main__":
    main()
