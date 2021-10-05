#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Openconfig YANG models to collect switchport
configs on a Cisco NX-OS switch via the always-on Cisco DevNet sandbox.
"""


import xmltodict
from ncclient import manager


def main():
    """
    Execution begins here.
    """

    # Dictionary containing keyword arguments (kwargs) for connecting
    # via NETCONF. Because SSH is the underlying transport, there are
    # several minor options to set up.
    connect_params = {
        "host": "sbx-nxos-mgmt.cisco.com",
        "port": 10000,
        "username": "admin",
        "password": "Admin_1234!",
        "hostkey_verify": False,
        "allow_agent": False,
        "look_for_keys": False,
        "device_params": {"name": "nexus"},
    }

    # Unpack the connect_params dict and use them to connect inside
    # of a "with" context manager. The variable "conn" represents the
    # NETCONF connection to the device.
    with manager.connect(**connect_params) as conn:
        print("NETCONF session connected")

        # To save time, only capture 3 switchports. Less specific filters
        # will return more information, but take longer to process/transport.
        # Note: In this sandbox, it can take ~30 seconds to get all interfaces
        # and several minutes to get the whole config, so be aware!
        nc_filter = """
            <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                    <name>eth1/71</name>
                </interface>
                <interface>
                    <name>eth1/72</name>
                </interface>
                <interface>
                    <name>eth1/73</name>
                </interface>
            </interfaces>
        """

        # Execute a "get-config" RPC using the filter defined above
        resp = conn.get_config(source="running", filter=("subtree", nc_filter))

        # Uncomment line below to see raw RPC XML reply; great for learning
        # print(resp.xml)

        # Parse the XML text into a Python dictionary
        jresp = xmltodict.parse(resp.xml)

        # Uncomment line below to see parsed JSON RPC; great for learning
        # import json; print(json.dumps(jresp, indent=2))

        # Iterate over all the interfaces returned by helper function
        for intf in jresp["rpc-reply"]["data"]["interfaces"]["interface"]:

            # Declare a few local variables to make accessing data deep
            # within the JSON structure a little easier
            config = intf["ethernet"]["switched-vlan"]["config"]
            mode = config["interface-mode"].lower()

            # Print common switchport data
            print(f"Name: {intf['name']:<7}  Type: {mode:<6}", end="  ")

            # Print additional data depending on access vs trunk ports
            if mode == "access":
                print(f"Access VLAN: {config['access-vlan']}")
            elif mode == "trunk":
                print(f"Native VLAN: {config['native-vlan']}")
            else:
                print("(no additional data)")

    print("NETCONF session disconnected")


if __name__ == "__main__":
    main()
