#!/usr/bin/env python

"""
Author: Nick Russo
File contains custom filters for use in Ansible playbooks.
"""

class FilterModule:
    """
    Defines a filter module object.
    """

    @staticmethod
    def filters():
        """
        Return a list of hashes where the key is the filter
        name exposed to playbooks and the value is the function.
        """
        return {"reform_vlans": FilterModule.reform_vlans}

    @staticmethod
    def reform_vlans(raw_vlans, strict_mode=False):
        """
        Converts the list of interfaces in each VLAN to the
        format required by NAPALM validation by adding a
        'list' key into the hierarchy, along with an optional
        '_mode' key for strict compliance checking.
        """

        # Create new VLAN dict and iterate over input VLANs
        new_vlans = {}
        napalm_vlans = raw_vlans["ansible_facts"]["napalm_vlans"]
        for vlan_id, vlan_attrs in napalm_vlans.items():

            # Perform a deep copy with all attributes first
            new_vlans.update({vlan_id: vlan_attrs})

            # Overwrite "interfaces" key with new structure
            new_vlans[vlan_id]["interfaces"] = {"list": vlan_attrs["interfaces"]}

            # Optionally add "_mode" key if strict mode is enabled
            if strict_mode:
                new_vlans[vlan_id]["interfaces"]["_mode"] = "strict"

        # Wrap the new VLAN dict in a list of dicts
        return [{"get_vlans": new_vlans}]
