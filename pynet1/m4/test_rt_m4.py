#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: The pytest functions for ensuring VRF configuration parsers
for IOS-XE and IOS-XR are functional. Run with "-s" to see outputs.
"""

from parse_rt_m4 import parse_rt_ios, parse_rt_iosxr


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
    assert not vrf_data["123"]["route_export"]  # tests len == 0
    assert len(vrf_data["123"]["route_import"]) == 1
    assert vrf_data["123"]["route_import"][0] == "65000:303"
