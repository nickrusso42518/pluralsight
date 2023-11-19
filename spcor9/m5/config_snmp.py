#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF to configure SNMP on IOS-XE/XR devices
based on a pre-made XML input file. Save config when complete.
"""

from lxml.etree import fromstring
from ncclient import manager
from ncclient.operations import RPCError


def main():
    """
    Execution begins here.
    """

    # Include OS, target datastore, and save_config function reference per host
    host_os_map = {
        "10.0.90.3": {
            "os": "csr",
            "ds": "running",
            "save": save_config_iosxe,
        },
        "10.0.90.12": {
            "os": "iosxr",
            "ds": "candidate",
            "save": save_config_iosxr,
        },
    }

    for host, attr in host_os_map.items():
        # Dictionary containing keyword arguments (kwargs) for connecting
        # via NETCONF. Because SSH is the underlying transport, there are
        # several minor options to set up.
        connect_params = {
            "host": host,
            "username": "labadmin",
            "password": "labadmin",
            "hostkey_verify": False,
            "allow_agent": False,
            "look_for_keys": False,
            "device_params": {"name": attr["os"]},
        }

        # Open OS-specific SNMP XML data (NETCONF payload) for reading
        with open(f"add_{attr['os']}_snmp.xml", "r") as handle:
            xpayload = handle.read()

        # Unpack the connect_params dict and use them to connect inside
        # of a "with" context manager. The variable "conn" represents the
        # NETCONF connection to the device.
        with manager.connect(**connect_params) as conn:
            print(f"{host}: NETCONF session connected")

            # Issue edit-config RPC to the proper target datastore with the
            # proper XML payload. Malformed payloads are common during
            # development, so print the error-info element data and keep
            # looping to try configuring the other routers.
            try:
                config_resp = conn.edit_config(target=attr["ds"], config=xpayload)
            except RPCError as rpc_error:
                print(f"{host}: RPCError received: \n{rpc_error.to_dict()}")
                continue

            # edit-config successful; print message
            print(f"{host}: Successfully modified {attr['ds']}-config")

            # If save operation succeeds, print "saved" message. You could
            # use try/except pattern again; this is just an alternative way
            if config_resp.ok and attr["save"](conn).ok:
                print(f"{host}: Successfully saved config changes")

        # Indicate disconnection when "with" context ends
        print(f"{host}: NETCONF session disconnected\n")


def save_config_iosxe(conn):
    """
    Copy running-config to startup-config on IOS-XE devices. This requires
    a custom RPC specific to IOS-XE.
    """

    save_rpc = '<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>'
    save_resp = conn.dispatch(fromstring(save_rpc))
    return save_resp


def save_config_iosxr(conn):
    """
    Commit candidate-config to running-config on IOS-XR devices. This is a
    standard NETCONF RPC with nothing special required.
    """

    commit_resp = conn.commit()
    return commit_resp


if __name__ == "__main__":
    main()
