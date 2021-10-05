#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Applies the policy described in the "policy_objects" files.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

from cisco_ftd import CiscoFTD


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

    # Get the security zones, which exist by default
    inside_zone = ftd.get_security_zones("inside_zone")["items"][0]
    outside_zone = ftd.get_security_zones("outside_zone")["items"][0]

    # Permit VPN sessions to headends from outside to inside
    vpn_rule = ftd.add_access_rule(
        rule_name="OUT_TO_IN_VPN",
        rule_action="PERMIT",
        rule_position=10,
        sourceZones=[outside_zone],
        destinationZones=[inside_zone],
        destinationNetworks=[vpn_resp],
        destinationPorts=[ipsec_resp],
    )

    # Deny traffic to documentation prefixes from inside to outside
    blacklist_rule = ftd.add_access_rule(
        rule_name="IN_TO_OUT_BLACKLIST",
        rule_action="DENY",
        rule_position=20,
        sourceZones=[inside_zone],
        destinationZones=[outside_zone],
        destinationNetworks=[blacklist_resp],
    )


def cleanup(ftd):
    """
    Quick cleanup function to make "starting over" easier. Also
    exercises many of the HTTP DELETE requests in the SDK.
    """
    ftd.delete_access_rule_name("IN_TO_OUT_BLACKLIST")
    ftd.delete_access_rule_name("OUT_TO_IN_VPN")
    ftd.purge_group_name("NETG_VPN_CONCENTRATORS", "networkobjectgroup")
    ftd.purge_group_name("NETG_BLACKLIST", "networkobjectgroup")
    ftd.purge_group_name("PORTG_IPSEC", "portobjectgroup")


if __name__ == "__main__":
    main()
