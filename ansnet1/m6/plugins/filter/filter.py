#!/usr/bin/python
"""
Author: Nick Russo <njrusmc@gmail.com>

File contains custom filters for use in Ansible playbooks.
https://www.ansible.com/
"""

import re

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
        return {
            'rt_diff': FilterModule.rt_diff
        }

    @staticmethod
    def rt_diff(int_vrf_list, run_vrf_dict):
        """
        Uses set theory to determine the import/export route-targets that
        should be added or deleted. Only differences are captured, which helps
        Ansible achieve idempotence when making configuration updates.
        """
        return_list = []
        for int_vrf in int_vrf_list:
            # Copy benign parameters from intended config
            vrf_dict = {
                'name': int_vrf['name'],
                'rd': int_vrf['rd'],
                'description': int_vrf['description']
            }

            # If the intended VRF exists in the running config
            run_vrf = run_vrf_dict.get(str(int_vrf['name']))
            if run_vrf:
                # Convert each list to a set
                int_rti = set(int_vrf['route_import'])
                int_rte = set(int_vrf['route_export'])
                run_rti = set(run_vrf['route_import'])
                run_rte = set(run_vrf['route_export'])

                # Perform set "difference" operation
                vrf_dict.update({'add_rti': list(int_rti - run_rti)})
                vrf_dict.update({'del_rti': list(run_rti - int_rti)})
                vrf_dict.update({'add_rte': list(int_rte - run_rte)})
                vrf_dict.update({'del_rte': list(run_rte - int_rte)})

            # Intended VRF doesn't exist, so add all the RTs
            else:
                vrf_dict.update({'add_rti': int_vrf['route_import']})
                vrf_dict.update({'del_rti': []})
                vrf_dict.update({'add_rte': int_vrf['route_export']})
                vrf_dict.update({'del_rte': []})

            # Add the newly created dictionary to the list of dicts
            return_list.append(vrf_dict)

        return return_list
