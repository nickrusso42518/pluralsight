#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Add global and reservable IP pools to the site
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
    with open("input_data/global_pool.json", "r") as handle:
        data = json.load(handle)

    # Create new global pool
    print("Adding global pool")
    add_resp = dnac.req("dna/intent/api/v1/global-pool", method="post", jsonbody=data)

    # Extract the executionStatusUrl and wait for it to finish being created
    status_url = add_resp.json()["executionStatusUrl"]
    dnac.wait_for_exec_status(status_url[1:])

    # Issue GET to learn ID of building for subpools
    print("Getting site (building) ID")
    params = {"name": "Global/Maryland/secretlab"}
    get_resp = dnac.req("dna/intent/api/v1/site", params=params)
    bld_id = get_resp.json()["response"][0]["id"]

    # Loop over each type of subpool
    for body_type in ["data_pool", "voice_pool"]:

        # Load in the JSON data into Python objects
        with open(f"input_data/{body_type}.json", "r") as handle:
            data = json.load(handle)

        # Issue an HTTP POST request to create the subpool, which
        # must reference the global pool in the URL
        print(f"Adding reservable {body_type} to site {bld_id}")
        add_resp = dnac.req(
            f"dna/intent/api/v1/reserve-ip-subpool/{bld_id}",
            method="post",
            jsonbody=data,
        )

        # Extract the executionStatusUrl and wait for it to finish being created
        status_url = add_resp.json()["executionStatusUrl"]
        dnac.wait_for_exec_status(status_url[1:])

        # Get the object just created so we can confirm it
        get_resp = dnac.req(
            "dna/intent/api/v1/reserve-ip-subpool", params={"siteId": bld_id}
        )
        obj_data = get_resp.json()["response"][0]
        print(f"{body_type} created with id {obj_data['id']}")


if __name__ == "__main__":
    main()
