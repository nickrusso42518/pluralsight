#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Cisco Native YANG models to manage OSPF/tunnel
features on a Cisco IOS-XE router in our test network.
"""


import xmltodict
import yaml
from lxml.etree import fromstring
from ncclient import manager


def main():
    """
    Execution begins here.
    """

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

            # Perform the update, and if success, print a message
            config_resp = update_wan(conn, "config_state.yml")

            # If config and save operations succeed, print "saved" message
            if config_resp.ok and save_config_iosxe(conn).ok:
                print("Successfully saved running-config to startup-config")

        print(f"NETCONF session disconnected: {host['name']}")


def update_wan(conn, filename):
    """
    Updates tunnel, keychain, and OSPF config based on YAML file. Expects that
    the NETCONF connection is already open and that all data is valid. Feel
    free to add more data validation here as a challenge.
    """

    # Load in the data from the specified file
    with open(filename, "r") as handle:
        data = yaml.safe_load(handle)

    # Assemble the payload based on the YANG structure. Using helper functions
    # can improve readability/maintainability as shown here.
    payload = {
        "config": {
            "native": {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
                "key": {"chain": build_keychain(data["security"]["key_chain"])},
                "interface": {
                    "Tunnel": build_tunnel(data["security"]["key_chain"])
                },
                "router": {"ospf": build_ospf(data["routing"])},
            }
        }
    }

    # Assemble the XML payload by "unparsing" the JSON dict (JSON --> XML)
    xpayload = xmltodict.unparse(payload)

    # Issue the NETCONF edit_config RPC to the running config; return response
    config_resp = conn.edit_config(target="running", config=xpayload)
    return config_resp


def build_tunnel(kc_dict):
    """
    Returns a YANG-structured dictionary that can be plugged into a Cisco
    IOS-XE native YANG data payload. Uses the supplied kc_dict to give
    access to all keychain related parameters. Includes a config snippet
    for Tunnel 100.
    """

    return {
        "name": "100",
        "ip": {
            "ospf": {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf",
                "authentication": {"key-chain": {"name": kc_dict["name"]}},
            }
        },
    }


def build_keychain(kc_dict):
    """
    Returns a YANG-structured dictionary that can be plugged into a Cisco
    IOS-XE native YANG data payload. Uses the supplied kc_dict to give
    access to all keychain related parameters. Includes a config snippet
    for the specific keychain.
    """

    return {
        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-crypto",
        "name": kc_dict["name"],
        "key": {
            "id": kc_dict["key"]["id"],
            "key-string": {"key": kc_dict["key"]["text"]},
            "cryptographic-algorithm": "hmac-sha-256",
        },
    }


def build_ospf(routing_dict):
    """
    Returns a YANG-structured dictionary that can be plugged into a Cisco
    IOS-XE native YANG data payload. Uses the supplied routing_dict to give
    access to all routing related parameters. Includes a config snippet
    for OSPF process ID 1.
    """

    return {
        "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf",
        "id": "1",
        "auto-cost": {"reference-bandwidth": routing_dict["ref_bw"]},
        "passive-interface": {"interface": ["Loopback0"]},
        "ttl-security": {
            "all-interfaces": None,
            "hops": routing_dict["ttl_security_hops"],
        },
    }


def save_config_iosxe(conn):
    """
    Save config on Cisco IOS-XE is complex and requires a custom RPC.
    Reference the IOS-XE programmability documentation for further details.
    """

    save_rpc = '<save-config xmlns="http://cisco.com/yang/cisco-ia"/>'
    save_resp = conn.dispatch(fromstring(save_rpc))
    return save_resp


if __name__ == "__main__":
    main()
