#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: The pytest functions for ensuring VRF configuration parsers
for IOS-XE and IOS-XR are functional. Run with "-s" to see outputs.
File renamed to "test_rt_pd" for "parse" and "diff" together.
"""

from parse_rt_m6 import parse_rt_ios, parse_rt_iosxr, get_rt_parser, rt_diff


def test_parse_rt_ios():
    """
    Defines unit tests for the Cisco IOS VRF route-target parser.
    """

    # Create and display some test data
    vrf_output = """
        vrf definition A
         description first VRF
         rd 65000:1
         route-target export 65000:111
         route-target import 65000:101
        !
        vrf definition VPN2
         description second VRF
         rd 65000:2
         route-target export 65000:111
         route-target export 65000:222
         route-target import 65000:101
         route-target import 65000:202
        !
        vrf definition 123
         description third VRF
         rd 65000:3
         route-target import 65000:303
        !
    """
    print(vrf_output)

    # Perform parsing, print structured data, and validate
    vrf_data = parse_rt_ios(vrf_output)
    print(vrf_data)
    _check_vrf_data(vrf_data)


def test_parse_rt_iosxr():
    """
    Defines unit tests for the Cisco IOS XR VRF route-target parser.
    """

    # Create and display some test data
    vrf_output = """
        vrf A
         description first VRF
         address-family ipv4 unicast
          import route-target
           65000:101
          !
          export route-target
           65000:111
          !
         !
        !
        vrf VPN2
         description second VRF
         address-family ipv4 unicast
          import route-target
           65000:101
           65000:202
          !
          export route-target
           65000:111
           65000:222
          !
         !
        !
        vrf 123
         description third VRF
         address-family ipv4 unicast
          import route-target
           65000:303
          !
         !
        !
    """
    print(vrf_output)

    # Perform parsing, print structured data, and validate
    vrf_data = parse_rt_iosxr(vrf_output)
    print(vrf_data)
    _check_vrf_data(vrf_data)


def test_get_rt_parser():
    """
    Test the dispatch mapper to ensure it returns the proper parsers
    """
    assert get_rt_parser("ios") == parse_rt_ios
    assert get_rt_parser("iosxr") == parse_rt_iosxr
    assert get_rt_parser("bogus") is None


def test_rt_diff():
    """
    Ensure the set theory logic functions correctly
    """
    run_vrf_dict = {
        "VPN1": {"route_import": ["65000:1"], "route_export": []},
        "VPN2": {
            "route_import": ["65000:222", "65000:1"],
            "route_export": ["65000:2"],
        },
        "VPN3": {"route_import": ["65000:2", "65000:333"], "route_export": []},
    }

    int_vrf_list = [
        {
            "name": "VPN1",
            "description": "first VRF",
            "rd": "65000:1",
            "route_import": ["65000:1"],
            "route_export": ["65000:2"],
        },
        {
            "name": "VPN2",
            "description": "second VRF",
            "rd": "65000:2",
            "route_import": ["65000:1"],
            "route_export": ["65000:2"],
        },
        {
            "name": "VPN3",
            "description": "third VRF",
            "rd": "65000:3",
            "route_import": ["65000:2"],
            "route_export": ["65000:1"],
        },
    ]

    # Perform set theory intersection of intended vs actual
    rt_updates = rt_diff(int_vrf_list, run_vrf_dict)

    # Check the VPN1 results
    assert len(rt_updates) == 3
    assert rt_updates[0]["name"] == "VPN1"
    assert rt_updates[0]["description"] == "first VRF"
    assert rt_updates[0]["rd"] == "65000:1"
    assert len(rt_updates[0]["add_rte"]) == 1
    assert rt_updates[0]["add_rte"][0] == "65000:2"
    assert rt_updates[0]["del_rte"] == []
    assert rt_updates[0]["add_rti"] == []
    assert rt_updates[0]["del_rti"] == []

    # Check the VPN2 results
    assert rt_updates[1]["name"] == "VPN2"
    assert rt_updates[1]["description"] == "second VRF"
    assert rt_updates[1]["rd"] == "65000:2"
    assert rt_updates[1]["add_rte"] == []
    assert rt_updates[1]["del_rte"] == []
    assert rt_updates[1]["add_rti"] == []
    assert len(rt_updates[1]["del_rti"]) == 1
    assert rt_updates[1]["del_rti"][0] == "65000:222"

    # Check the VPN3 results
    assert rt_updates[2]["name"] == "VPN3"
    assert rt_updates[2]["description"] == "third VRF"
    assert rt_updates[2]["rd"] == "65000:3"
    assert len(rt_updates[2]["add_rte"]) == 1
    assert rt_updates[2]["add_rte"][0] == "65000:1"
    assert rt_updates[2]["del_rte"] == []
    assert rt_updates[2]["add_rti"] == []
    assert len(rt_updates[2]["del_rti"]) == 1
    assert rt_updates[2]["del_rti"][0] == "65000:333"


def _check_vrf_data(vrf_data):
    """
    Common asserts for all parsers
    """

    # Returned dict should have exactly 3 keys
    assert len(vrf_data) == 3

    # Ensure VRF A parsing succeeded
    assert len(vrf_data["A"]["route_export"]) == 1
    assert vrf_data["A"]["route_export"][0] == "65000:111"
    assert len(vrf_data["A"]["route_import"]) == 1
    assert vrf_data["A"]["route_import"][0] == "65000:101"

    # Ensure VRF VPN2 parsing succeeded
    assert len(vrf_data["VPN2"]["route_export"]) == 2
    assert vrf_data["VPN2"]["route_export"][0] == "65000:111"
    assert vrf_data["VPN2"]["route_export"][1] == "65000:222"
    assert len(vrf_data["VPN2"]["route_import"]) == 2
    assert vrf_data["VPN2"]["route_import"][0] == "65000:101"
    assert vrf_data["VPN2"]["route_import"][1] == "65000:202"

    # Ensure VRF 123 parsing succeeded
    assert vrf_data["123"]["route_export"] == []
    assert len(vrf_data["123"]["route_import"]) == 1
    assert vrf_data["123"]["route_import"][0] == "65000:303"
