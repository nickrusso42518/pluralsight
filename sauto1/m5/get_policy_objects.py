#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets the current policy objects from the FMC sandbox.
Check out the API explorer at "https://<fmc_host>/api/api-explorer"
"""

from cisco_fmc import CiscoFMC


def main():
    """
    Execution begins here.
    """

    # Create a new FMC object referencing the DevNet sandbox (default)
    fmc = CiscoFMC.build_from_env_vars()

    # List of resources to query; basically, network and port/protocol objects
    # The second item in the tuple is the "value of interest" which may even
    # contain multiple keys, represented by a nested list
    resource_list = [
        ("object/networks", ["value"]),
        ("object/hosts", ["value"]),
        ("object/networkgroups", None),
        ("object/protocolportobjects", ["port", "protocol"]),
        ("object/portobjectgroups", None),
    ]

    # Iterate over the list of specified resource/key tuples
    for resource, keys in resource_list:

        # Issue a GET request to collect a list of network objects configured
        # on the FMC device. Raise HTTPErrors if the request fails
        get_resp = fmc.req(resource, params={"limit": 3})

        # Iterate over each item in the "items" list returned by the API
        for item in get_resp["items"]:

            # Print the name, type, and "value of interest" for
            # each item in the list if the key is defined/truthy
            print(f"\nname: {item['name']} / {item['type']}")

            # We need to go one step deeper to query the individual items
            # as FMC does not reveal any details by default. Use the UUID
            obj_data = fmc.req(f"{resource}/{item['id']}")
            if keys:
                for key in keys:
                    print(f"{key}: {obj_data[key]}")

            # If the "objects" key is present and is a list, iterate
            # over that list and print the name and type of each object
            if "objects" in item and isinstance(item["objects"], list):
                print("Contained objects:")
                for obj in item["objects"]:
                    print(f"  - {obj['name']} / {obj['type']}")


if __name__ == "__main__":
    main()
