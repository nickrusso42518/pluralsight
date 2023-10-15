#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to use the various site URLs
to create a new site and assign devices to it.
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
        host="198.18.129.100", username="admin", password="C1sco12345", verify=False
    )

    # Loop over each type of site object (this time, no floor)
    for body_type in ["area", "building"]:

        # Load in the JSON data into Python objects
        with open(f"input_data/{body_type}.json", "r") as handle:
            data = json.load(handle)

        # Declare some local variables and print a status message
        site = data["site"][body_type]
        name = f"{site['parentName']}/{site['name']}"
        print(f"Adding {body_type} object {name}")

        # Issue an HTTP POST request to create the site object
        add_resp = dnac.req(
            "dna/intent/api/v1/site", method="post", jsonbody=data
        )

        # Extract the executionStatusUrl and wait for it to finish being created
        status_url = add_resp.json()["executionStatusUrl"]
        dnac.wait_for_exec_status(status_url[1:])

        # Get the object just created so we can optionally print it out
        get_resp = dnac.req("dna/intent/api/v1/site", params={"name": name})
        obj_data = get_resp.json()["response"][0]

        print(f"Object created with id {obj_data['id']}")


if __name__ == "__main__":
    main()
