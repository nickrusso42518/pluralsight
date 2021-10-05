#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Gets the current policy summary from the FTD sandbox.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

from cisco_ftd import CiscoFTD


def main():
    """
    Execution begins here.
    """

    # Create a new FTD object referencing the DevNet sandbox (default)
    ftd = CiscoFTD()

    # Issue a GET request to collect a list of access policies configured
    # on the FTD device. Raise HTTPErrors if the request fails. This is a
    # bit redundant and could be optimized if the constructor changed
    ap_resp = ftd.req("policy/accesspolicies")

    # Each rule has at least these 6 lists for src/dest zones,
    # networks, and ports. Can also include non-lists like IPS
    # policy (add whatever else you like)
    components = [
        "sourceZones",
        "destinationZones",
        "sourceNetworks",
        "destinationNetworks",
        "sourcePorts",
        "destinationPorts",
        "intrusionPolicy",
    ]

    # Iterate over all of the access policies (typically only one)
    for policy in ap_resp["items"]:
        print(f"Policy name: {policy['name']}")

        # Get the rules within the policy by UUID
        rule_resp = ftd.req(f"policy/accesspolicies/{policy['id']}/accessrules")

        # Iterate over the rules defined in the policy
        for rule in rule_resp["items"]:
            print(f"  Rule name: {rule['name']} -> {rule['ruleAction']}")

            # Print source/destination components, one line each
            for comp in components:

                # If the component is a list, get all the item names
                if isinstance(rule[comp], list):
                    names = [item["name"] for item in rule[comp]]

                    # Only print the data if it exists; ignore empty lists
                    if names:
                        print(f"    {comp}: {','.join(names)}")

                # If the component is a dict, just print the item name
                elif isinstance(rule[comp], dict):
                    print(f"    {comp}: {rule[comp]['name']}")


if __name__ == "__main__":
    main()
