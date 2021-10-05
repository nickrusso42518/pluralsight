#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Applies the policy described in the "policy_objects" files.
Check out the API explorer at "https://<fmc_host>/api/api-explorer"
"""

from cisco_fmc import CiscoFMC


def main():
    """
    Execution begins here.
    """

    # Create a new FMC object referencing the DevNet sandbox (default)
    fmc = CiscoFMC.build_from_env_vars()

    # Create VPN network, IPsec port/protocol, and blacklist network groups
    vpn_resp = fmc.add_group_file("objects/group_vpn.json")
    blacklist_resp = fmc.add_group_file("objects/group_blacklist.json")
    ipsec_resp = fmc.add_group_file("objects/group_ipsec.json")

    # Cannot always filter by name in FMC, so use an interactive technique
    cleanup = input("Purge items just added? (y/n): ").lower()

    if cleanup == "y":

        # Delete custom policy objects recursively (groups and components)
        fmc.purge_group_id(vpn_resp["id"], "NetworkGroup")
        fmc.purge_group_id(blacklist_resp["id"], "NetworkGroup")
        fmc.purge_group_id(ipsec_resp["id"], "PortObjectGroup")


if __name__ == "__main__":
    main()
