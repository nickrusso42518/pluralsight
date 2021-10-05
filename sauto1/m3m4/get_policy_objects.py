#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets the current policy objects from the FTD sandbox.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

from cisco_ftd import CiscoFTD


def main():
    """
    Execution begins here.
    """

    # Create a new FTD object referencing the DevNet sandbox (default)
    ftd = CiscoFTD()

    # List of resources to query; basically, network and port/protocol objects
    # The second item in the tuple is the "value of interest" which varies
    resource_list = [
        ("object/networks", "value"),
        ("object/tcpports", "port"),
        ("object/udpports", "port"),
        ("object/protocols", "protocol"),
        ("object/networkgroups", None),
        ("object/portgroups", None),
    ]

    # Iterate over the list of specified resource/key tuples
    for resource, key in resource_list:

        # Issue a GET request to collect a list of network objects configured
        # on the FTD device. Raise HTTPErrors if the request fails
        get_resp = ftd.req(resource)

        # Iterate over each item in the "items" list returned by the API
        for item in get_resp["items"]:

            # Print the name, type, and "value of interest" for
            # each item in the list if the key is defined/truthy
            print(f"\nName: {item['name']} / {item['type']}")
            if key:
                print(f"{key}: {item[key]}")

            # If the "objects" key is present and is a list,
            # iterate over that list and print the name of each object
            if "objects" in item and isinstance(item["objects"], list):
                print("Contained objects:")
                for obj in item["objects"]:
                    print(f"  - {obj['name']}")


if __name__ == "__main__":
    main()
