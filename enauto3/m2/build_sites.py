#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the various site URLs
to create a new site and assign devices to it.
"""

import json
import time
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    # Loop over each type of site object
    for body_type in ["area", "building", "floor"]:

        # Load in the JSON data into Python objects
        with open(f"site_data/{body_type}.json", "r") as handle:
            data = json.load(handle)

        # Declare some local variables and print a status message
        site = data["site"][body_type]
        name = f"{site['parentName']}/{site['name']}"
        print(f"Adding {body_type} object {name}")

        # Issue an HTTP POST request to create the site object
        add_resp = dnac.req(
            "dna/intent/api/v1/site", method="post", jsonbody=data
        )

        # Debugging statement to ensure sites were added
        # print(json.dumps(add_resp.json(), indent=2))

        # Extract the executionStatusUrl and wait for it to finish being created
        status_url = add_resp.json()["executionStatusUrl"]
        status_resp = wait_for_site_creation(dnac, status_url[1:])

        # Ensure the creation succeeded; always returns a successful HTTP
        # status code, so check the "status" key explicitly
        if status_resp.json()["status"].lower() != "success":
            raise ValueError("Site object addition failed")

        # Get the object just created so we can optionally print it out
        get_resp = dnac.req("dna/intent/api/v1/site", params={"name": name})
        obj_data = get_resp.json()["response"][0]

        # Debugging statement to ensure sites were added
        # print(json.dumps(get_resp.json(), indent=2))

        # Special case; store the floor ID so we can assign devices to it later
        if body_type == "floor":
            floor_id = obj_data["id"]

        print(f"Object created with id {obj_data['id']}")

    # Load in dummy device body from JSON file
    with open(f"site_data/device.json", "r") as handle:
        data = json.load(handle)

    # Issue HTTP POST to add dummy device
    add_dev_resp = dnac.req(
        "dna/intent/api/v1/network-device", method="post", jsonbody=data
    )

    # Optionally print out the JSON data associated with creating the object
    # print(json.dumps(add_dev_resp.json(), indent=2))

    # Need to wait for device to be added, but don't care about return data
    dnac.wait_for_task(add_dev_resp.json()["response"]["taskId"])

    # Assign the new device to the floor by specifying its IP address in
    # the request body
    new_ip = data["ipAddress"][0]
    assign_dev_resp = dnac.req(
        f"dna/system/api/v1/site/{floor_id}/device",
        method="post",
        jsonbody={"device": [{"ip": new_ip}]},
    )

    # Optionally print out the JSON data associated with creating the object
    # print(json.dumps(assign_dev_resp.json(), indent=2))

    # Capture the status URL and wait for the device addition to be completed
    status_url = assign_dev_resp.json()["executionStatusUrl"]
    status_resp = wait_for_site_creation(dnac, status_url[1:])

    # Confirm that the device is a "member" of the floor
    mem_resp = dnac.req(f"dna/intent/api/v1/membership/{floor_id}")

    # Print the membership response for debugging
    # print(json.dumps(mem_resp.json(), indent=2))

    # Perform a quick sanity check to ensure the IP address just added matches
    # the IP address specified in the POST request
    added_ip = mem_resp.json()["device"][0]["response"][0]["managementIpAddress"]
    if new_ip != added_ip:
        raise ValueError(f"IP addresses don't match: {new_ip} != {added_ip}")

    # Print final status message
    print(f"Assigned device to floor {floor_id} with IP address {new_ip}")


def wait_for_site_creation(dnac, status_url, wait_time=5):
    """
    Local helper function to wait for individual site objects to be created.
    This API is asynchronous and uses HTTP status 202, but does not use the
    same "task ID" query process as most other DNA Center tasks.
    """
    done = False

    # Continue looping while we are not done
    while not done:
        time.sleep(wait_time)

        # After waiting, issue the request and see if the task is in progress
        status_resp = dnac.req(status_url)
        done = status_resp.json()["status"].lower() != "in_progress"
    return status_resp


if __name__ == "__main__":
    main()
