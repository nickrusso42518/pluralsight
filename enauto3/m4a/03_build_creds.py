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

    # Loop over each type of credential object (name = URL endpoint)
    cred_keys = ["cliId", "snmpV2ReadId", "snmpV2WriteId"]
    cred_urls = ["cli", "snmpv2-read-community", "snmpv2-write-community"]
    cred_activate = {}
    for i, body_type in enumerate(cred_urls):

        # Load in the JSON data into Python objects
        with open(f"input_data/{body_type}.json", "r") as handle:
            data = json.load(handle)

        # Issue an HTTP POST request to create the credential
        print(f"Adding {body_type} global credential")
        add_resp = dnac.req(
            f"dna/intent/api/v1/global-credential/{body_type}",
            method="post",
            jsonbody=data,
        )

        # This API uses standard tasks; wait for completion
        task_resp = dnac.wait_for_task(add_resp.json()["response"]["taskId"])

        # Store credential ID, print it, and add to activation dict
        cred_id = task_resp.json()["response"]["progress"]
        print(f"Added {body_type} with ID {cred_id}")
        cred_activate[cred_keys[i]] = cred_id

    # Print credential dict for visual confirmation
    print(f"Cred activation dict: {json.dumps(cred_activate, indent=2)}")

    # Issue GET to learn ID of global site
    print("Getting global site ID")
    params = {"name": "Global"}
    get_resp = dnac.req("dna/intent/api/v1/site", params=params)
    global_id = get_resp.json()["response"][0]["id"]

    # Assign credentials to global site using credential dict as body
    print(f"Assigning creds to {global_id}")
    assign_resp = dnac.req(
        f"dna/intent/api/v1/credential-to-site/{global_id}",
        method="post",
        jsonbody=cred_activate,
    )

    # Extract the executionStatusUrl and wait for it to finish being created
    status_url = assign_resp.json()["executionStatusUrl"]
    dnac.wait_for_exec_status(status_url[1:])


if __name__ == "__main__":
    main()
