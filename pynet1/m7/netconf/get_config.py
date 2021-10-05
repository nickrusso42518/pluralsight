#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate NETCONF on IOS-XE and IOS-XR to collect
VRF configuration using the get-config RPC with ncclient.
"""

from ncclient import manager
from lxml.etree import tostring


def main():
    """
    Execution starts here. Not using Nornir because NETCONF plugin
    has not been authored yet. Read more here:
    https://github.com/nornir-automation/nornir/issues/208
    """

    # Iterate over the list of hosts (string) defined below.
    # Refreshing the simple "in-line" inventory concept.
    xr_xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-infra-rsi-cfg"
    host_dict = {
        "R1": "<native><vrf></vrf></native>",
        "R2": f'<vrfs xmlns="{xr_xmlns}"></vrfs>',
    }

    for hostname, vrf_filter in host_dict.items():
        # Open a new NETCONF connection to each host using kwargs technique
        connect_params = {
            "host": hostname,
            "username": "pyuser",
            "password": "pypass",
            "hostkey_verify": False,
            "allow_agent": False,
            "look_for_keys": False,
        }

        # Use the dict above as "keyword arguments" to open netconf session
        with manager.connect(**connect_params) as conn:

            # Gather the current XML configuration and pretty-print it
            print(f"{hostname}: Connection open")
            get_resp = conn.get_config(
                source="running", filter=("subtree", vrf_filter)
            )
            if get_resp.ok:
                # RPC worked; print the config with header/trailer
                print(f"{hostname}: VRF configuration start")
                xml_config = tostring(get_resp.data_ele, pretty_print=True)
                print(xml_config.decode().strip())
                print(f"{hostname}: VRF configuration end")
            else:
                # RPC failed; print list of errors as a comma-separated list
                print(f"{hostname}: Errors: {','.join(get_resp.errors)}")


if __name__ == "__main__":
    main()
