#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Cisco IOS-XE native YANG models to collect
OSPF, key chain, and tunnel configurations relevant to the network.
"""


import os
import json
import yaml
import xmltodict
from ncclient import manager


def main():
    """
    Execution begins here.
    """

    # Create outputs/ directory if it doesn't already exist
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = yaml.safe_load(handle)

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["production"]:

        # Dictionary containing keyword arguments (kwargs) for connecting
        # via NETCONF. Because SSH is the underlying transport, there are
        # several minor options to set up.
        connect_params = {
            "host": host["name"],
            "username": "cisco",
            "password": "cisco",
            "hostkey_verify": False,
            "allow_agent": False,
            "look_for_keys": False,
            "device_params": {"name": "csr"},
        }

        # Unpack the connect_params dict and use them to connect inside
        # of a "with" context manager. The variable "conn" represents the
        # NETCONF connection to the device.
        with manager.connect(**connect_params) as conn:
            print(f"NETCONF session connected: {host['name']}")

            # Craft a relatively complex subtree filter. This allows for granular
            # queries to minimize the data transferred and the load placed on
            # the NETCONF server.
            cfg_filter = """
                <native>
                  <interface>
                    <Tunnel>
                      <name>100</name>
                    </Tunnel>
                  </interface>
                  <key>
                    <chain xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto">
                      <name>KC_OSPF_AUTH</name>
                    </chain>
                  </key>
                  <router>
                    <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                      <id>1</id>
                    </ospf>
                  </router>
                </native>
            """.strip()

            # Execute a "get-config" RPC using the filter defined above
            resp = conn.get_config(
                source="running", filter=("subtree", cfg_filter)
            )

            # Uncomment line below to see raw RPC XML reply; great for learning
            # print(resp.xml)

            # Parse the XML text into a Python dictionary
            jresp = xmltodict.parse(resp.xml)

            # Store JSON-formatted YANG config data in host-specific files
            with open(f"outputs/{host['name']}_config.json", "w") as handle:
                json.dump(jresp, handle, indent=2)

        print(f"NETCONF session disconnected: {host['name']}")


if __name__ == "__main__":
    main()
