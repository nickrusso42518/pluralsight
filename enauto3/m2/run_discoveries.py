#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the network discovery tool on
Cisco DNA center via API calls.
"""

import json
import time
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

    # Collect the existing sandbox global credentials. Discoveries require a
    # minimum of CLI (ssh/telnet) and SNMPv2 read/write communities. This
    # requires individual GET requests using the credential type as a
    # query parameter.
    cred_list = []
    cred_types = ["CLI", "SNMPV2_READ_COMMUNITY", "SNMPV2_WRITE_COMMUNITY"]
    for cred in cred_types:
        cred_resp = dnac.req(
            "dna/intent/api/v1/global-credential",
            params={"credentialSubType": cred},
        )

        # Note: The reservable sandbox has exactly one of each type, so we can
        # safely index the first element. You may want to be more specific in
        # searching for credentials in your environment.
        cred_id = cred_resp.json()["response"][0]["id"]
        cred_list.append(cred_id)
        print(f"Collected {cred} credential with ID {cred_id}")

    # Load in a list of dictionaries containing the discovery parameters.
    # DNAC appears to only run one discovery at a time, so concurrency
    # would be meaningless; use a simple "for" loop
    with open("discoveries.json", "r") as handle:
        discoveries = json.load(handle)

    # Loop over each dictionary, update the dict with the credential list,
    # and run the discovery on the existing "dnac" object
    for disc_body in discoveries:
        disc_body["globalCredentialIdList"] = cred_list
        run_discovery(dnac, disc_body)


def run_discovery(dnac, disc_body, timeout=600):
    """
    Given an existing dnac object and a discovery payload, this function
    performs the following actions:
      1. Creates a new discovery
      2. Waits specified timeout for discovery to complete (default 10 min)
      3. Creates discovered_devices/ directory with subdirs for each discovery
      4. For reachable devices, writes discovery and device details to disk
    """

    # Create the discovery
    disc_resp = dnac.req(
        "dna/intent/api/v1/discovery", method="post", jsonbody=disc_body
    )

    # Wait for async job to complete. Note that this only measures
    # whether the discovery is created, not whether the discovery
    # process is complete
    disc_task = dnac.wait_for_task(disc_resp.json()["response"]["taskId"])
    disc_id = disc_task.json()["response"]["progress"]

    # Begin looping to see if the discovery process is complete. Any other
    # status should be printed out
    success = False
    for i in range(timeout // 10):

        # Get discovery by ID to see if it has completed
        get_disc = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}")
        data = get_disc.json()["response"]

        # If not complete, print the current condition and wait 10 seconds
        if data["discoveryCondition"].lower() != "complete":
            print(f"Discovery {disc_id} {data['discoveryCondition']} {i}")
            time.sleep(10)

        # Else discovery is complete, print number of devices found and exit loop
        else:
            print(f"Discovery {disc_id} found {data['numDevices']} devices")
            success = True
            break

    # If success is still false, raise a TimeoutError
    if not success:
        raise TimeoutError("Discovery did not complete in time")

    # Discovery succeeded; build the directories needed
    file_dir = f"disc_output/{disc_id}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Get a list of discovered devices and their statuses
    dev_sum = dnac.req(f"dna/intent/api/v1/discovery/{disc_id}/network-device")

    # Iterate over the discovered device list
    for dev in dev_sum.json()["response"]:

        # If devices were reachable via CLI or SNMPv2 ...
        if dev["reachabilityStatus"].lower() == "success":
            print(f"{dev['hostname']} success")

            # ... and they are already in the system as managed devices,
            # collect extra details, and write it to disk
            if dev["inventoryReachabilityStatus"].lower() == "reachable":
                get_dev = dnac.req(
                    f"dna/intent/api/v1/network-device/{dev['id']}"
                )

                # Create a top-level dict with "discovery" and "device" keys
                output = {"discovery": dev, "device": get_dev.json()["response"]}
                with open(f"{file_dir}/{dev['hostname']}.json", "w") as handle:
                    json.dump(output, handle, indent=2)

        # Else, discovery failed, so print the device IP address and reason
        else:
            print(
                f"Device {dev['managementIpAddress']} "
                f"failed: {dev['reachabilityFailureReason']}"
            )


if __name__ == "__main__":
    main()
