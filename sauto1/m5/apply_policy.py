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

    # Get the security zones, which exist by default
    inside_zone = fmc.get_security_zones("inside-zone")["items"][0]
    outside_zone = fmc.get_security_zones("outside-zone")["items"][0]

    # Create new access policy and extract the policy ID
    globo_policy = fmc.add_access_policy(
        name="GLOBO_POLICY",
        description="General VPN access and blacklist protection",
    )
    policy_id = globo_policy["id"]

    # Collect the IPS policy first as we'll need it for the VPN rule
    ips_resp = fmc.get_ips_policies(name="Balanced Security and Connectivity")

    # Permit VPN sessions to headends from outside to inside. Also
    # include the IPS policy from the beginning by extracting the
    # first (and only) item returned from the earlier API call
    vpn_rule = fmc.add_access_rule(
        name="OUT_TO_IN_VPN",
        action="ALLOW",
        policy_id=policy_id,
        sourceZones={"objects": [outside_zone]},
        destinationZones={"objects": [inside_zone]},
        destinationNetworks={"objects": [vpn_resp]},
        destinationPorts={"objects": [ipsec_resp]},
        ipsPolicy=ips_resp["items"][0],
    )

    # Deny traffic to documentation prefixes from inside to outside
    blacklist_rule = fmc.add_access_rule(
        name="IN_TO_OUT_BLACKLIST",
        action="BLOCK",
        policy_id=policy_id,
        sourceZones={"objects": [inside_zone]},
        destinationZones={"objects": [outside_zone]},
        destinationNetworks={"objects": [blacklist_resp]},
    )

    # Add in a general "permit any" from inside to outside zones by default
    default_rule = fmc.add_access_rule(
        name="IN_TO_OUT_GENERAL",
        action="ALLOW",
        policy_id=policy_id,
        sourceZones={"objects": [inside_zone]},
        destinationZones={"objects": [outside_zone]},
    )

    # Get the default device group
    default_group = fmc.get_device_groups(name="DefaultDeviceGroup")

    # Assign the new policy to the default device group
    assign = fmc.assign_group_to_policy(
        group=default_group["items"][0], policy=globo_policy
    )

    # Cannot always filter by name in FMC, so use an interactive technique
    cleanup = input("Purge items just added? (y/n): ").lower()

    if cleanup == "y":

        # Delete custom access policy; deletes all rules automatically
        fmc.delete_access_policy(policy_id)

        # Delete custom policy objects recursively (groups and components)
        fmc.purge_group_id(vpn_resp["id"], "NetworkGroup")
        fmc.purge_group_id(blacklist_resp["id"], "NetworkGroup")
        fmc.purge_group_id(ipsec_resp["id"], "PortObjectGroup")


if __name__ == "__main__":
    main()
