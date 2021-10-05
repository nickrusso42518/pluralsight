#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Applies the policy described in the "policy_objects" files.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

from cisco_ftd_obj2 import CiscoFTD  # change back


def main():
    """
    Execution begins here.
    """

    # Create a new FTD object referencing the DevNet sandbox (default)
    ftd = CiscoFTD()

    # Optional cleanup tasks; useful for testing to save time
    cleanup(ftd)

    # Create VPN network, IPsec port/protocol, and blacklist network groups
    vpn_resp = ftd.add_group_file("objects/group_vpn.json")
    ipsec_resp = ftd.add_group_file("objects/group_ipsec.json")
    blacklist_resp = ftd.add_group_file("objects/group_blacklist.json")


def cleanup(ftd):
    """
    Quick cleanup function to make "starting over" easier. Also
    exercises many of the HTTP DELETE requests in the SDK.
    """
    ftd.purge_group_name("NETG_VPN_CONCENTRATORS", "networkobjectgroup")
    ftd.purge_group_name("NETG_BLACKLIST", "networkobjectgroup")
    ftd.purge_group_name("PORTG_IPSEC", "portobjectgroup")


if __name__ == "__main__":
    main()
