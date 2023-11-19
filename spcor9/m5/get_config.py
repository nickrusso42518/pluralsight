#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF to collect IOS-XE/XR running configurations
and write them to disk in XML format.
"""

from ncclient import manager


def main():
    """
    Execution begins here.
    """

    # Include OS, target datastore, and save_config function reference per host
    host_os_map = {
        "10.0.90.3": "csr",
        "10.0.90.12": "iosxr",
    }

    for host, os in host_os_map.items():
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
            "device_params": {"name": os},
        }

        # Unpack the connect_params dict and use them to connect inside
        # of a "with" context manager. The variable "conn" represents the
        # NETCONF connection to the device.
        with manager.connect(**connect_params) as conn:
            print(f"{host}: NETCONF session connected")
            get_resp = conn.get_config(source="running")
            with open(f"data_ref/{host}_config.xml", "w") as handle:
                handle.write(get_resp.xml)

        # Indicate disconnection when "with" context ends
        print(f"{host}: NETCONF session disconnected\n")


if __name__ == "__main__":
    main()
