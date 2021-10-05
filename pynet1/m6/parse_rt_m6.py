#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Develop VRF configuration parsers for IOS-XE and IOS-XR.
These are focused on route-targets and not general-purpose VRF fields.
"""

import re


def parse_rt_ios(text):
    """
    Parses blocks of VRF text into indexable dictionary entries. This
    typically feeds into the rt_diff function to be tested against the
    intended config.
    """
    vrf_list = ["vrf" + s for s in text.strip().split("vrf") if s]
    return_dict = {}
    for vrf in vrf_list:
        # Parse the VRF name from the definition line
        name_regex = re.compile(r"vrf\s+definition\s+(?P<name>\S+)")
        name_match = name_regex.search(vrf)
        sub_dict = {}
        vrf_dict = {name_match.group("name"): sub_dict}

        # Parse the RT imports into a list of strings
        rti_regex = re.compile(r"route-target\s+import\s+(?P<rti>\d+:\d+)")
        rti_matches = rti_regex.findall(vrf)
        sub_dict.update({"route_import": rti_matches})

        # Parse the RT exports into a list of strings
        rte_regex = re.compile(r"route-target\s+export\s+(?P<rte>\d+:\d+)")
        rte_matches = rte_regex.findall(vrf)
        sub_dict.update({"route_export": rte_matches})

        # Append dictionary to return list
        return_dict.update(vrf_dict)

    return return_dict


def parse_rt_iosxr(text):
    """
    Parses blocks of VRF text into indexable dictionary entries. This
    typically feeds into the rt_diff function to be tested against the
    intended config.
    """
    vrf_list = ["vrf" + s for s in text.strip().split("vrf") if s]
    return_dict = {}
    for vrf in vrf_list:
        # Parse the VRF name from the definition line
        name_regex = re.compile(r"^vrf\s+(?P<name>\S+)")
        name_match = name_regex.search(vrf)
        sub_dict = {}
        vrf_dict = {name_match.group("name"): sub_dict}

        # Capture all text in between the start of "import route-target"
        # and the first exclamation mark to grab all import RTs
        rti_list = _get_iosxr_rt(r"import\s+route-target(.+?)!", vrf)
        sub_dict.update({"route_import": rti_list})

        # Repeat the same process for export RTs
        rte_list = _get_iosxr_rt(r"export\s+route-target(.+?)!", vrf)
        sub_dict.update({"route_export": rte_list})

        # Append dictionary to return list
        return_dict.update(vrf_dict)

    return return_dict


def _get_iosxr_rt(regex_str, vrf_str):
    """
    Internal-only function to parse IOS XR route targets from
    a VRF text output. This is a better design pattern than
    copy/paste, which was done for the IOS parser.
    """
    regex = re.compile(regex_str, re.DOTALL)
    rt_matches = regex.findall(vrf_str, re.DOTALL)
    if rt_matches:
        rt_list = [s.strip() for s in rt_matches[0].strip().split("\n")]
    else:
        rt_list = []

    # Return the list of parsed route-targets
    return rt_list


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
            "name": int_vrf["name"],
            "rd": int_vrf["rd"],
            "description": int_vrf["description"],
        }

        # If the intended VRF exists in the running config
        run_vrf = run_vrf_dict.get(str(int_vrf["name"]))
        if run_vrf:
            int_rti = set(int_vrf["route_import"])
            int_rte = set(int_vrf["route_export"])
            run_rti = set(run_vrf["route_import"])
            run_rte = set(run_vrf["route_export"])
            vrf_dict.update({"add_rti": list(int_rti - run_rti)})
            vrf_dict.update({"del_rti": list(run_rti - int_rti)})
            vrf_dict.update({"add_rte": list(int_rte - run_rte)})
            vrf_dict.update({"del_rte": list(run_rte - int_rte)})

        # intended VRF doesn't exist, so add all the RTs
        else:
            vrf_dict.update({"add_rti": int_vrf["route_import"]})
            vrf_dict.update({"del_rti": []})
            vrf_dict.update({"add_rte": int_vrf["route_export"]})
            vrf_dict.update({"del_rte": []})

        # Add the newly created dictionary to the list of dicts
        return_list.append(vrf_dict)

    return return_list


def get_rt_parser(platform):
    """
    Selects the proper parsing function based on the specific platform.
    Note it does not call the function, just returns it for calling later.
    """
    dispatch_dict = {"ios": parse_rt_ios, "iosxr": parse_rt_iosxr}
    return dispatch_dict.get(platform.lower())
