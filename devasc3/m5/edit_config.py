#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with Openconfig YANG models to manage Ethernet
VLANs on a Cisco NX-OS switch via the always-on Cisco DevNet sandbox.
"""


import xmltodict
import yaml
from lxml.etree import fromstring
from ncclient import manager
from ncclient.operations import RaiseMode


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

        # Perform the update, and if success, print a message
        config_resp = update_intf(conn, "config_state.yml")

        # If config and save operations succeed, print "saved" message
        if config_resp.ok and save_config_nxos(conn).ok:
            print("Successfully saved running-config to startup-config")

    print("NETCONF session disconnected")


def update_intf(conn, filename):
    """
    Updates switchports with new config based on YAML file. Expects that the
    NETCONF connection is already open and that all data is valid. Feel
    free to add more data validation here as a challenge.
    """

    with open(filename, "r") as handle:
        intfs_to_update = []
        config_state = yaml.safe_load(handle)
        for name, config in config_state["intf"].items():

            # NETCONF edit-config RPC payload which defines interface to update.
            # This follows the YANG model we explored in the get-config section.
            intfs_to_update.append(
                {
                    "name": name,
                    "ethernet": {
                        "@xmlns": "http://openconfig.net/yang/interfaces/ethernet",
                        "switched-vlan": {
                            "@xmlns": "http://openconfig.net/yang/vlan",
                            "config": config,
                        },
                    },
                }
            )

    # Assemble correct payload structure containing interface list, along
    # with any other items to be updated
    config_dict = {
        "config": {
            "interfaces": {
                "@xmlns": "http://openconfig.net/yang/interfaces",
                "interface": intfs_to_update,
            }
        }
    }

    # Assemble the XML payload by "unparsing" the JSON dict (JSON --> XML)
    xpayload = xmltodict.unparse(config_dict)

    # Secure a "lock" to prevent other NETCONF clients from configuring
    # the system concurrently. The lock is released automatically after
    # the "with" context exits.
    with conn.locked(target="candidate"):

        # We could change the "running" datastore directly, but using
        # the "candidate" option gives us the option to discard changes.
        # By changing the RaiseMode to NONE, we tell ncclient not to raise
        # errors, but instead to pass along the rpc-error. We change it
        # back to ALL after this RPC call so future RPCs will raise errors.
        conn.raise_mode = RaiseMode.NONE
        config_resp = conn.edit_config(target="candidate", config=xpayload)
        val_resp = conn.validate(source="candidate")
        conn.raise_mode = RaiseMode.ALL

        if config_resp.ok and val_resp.ok:
            # We need to "commit" from "candidate" to "running" config, an
            # intermediate step not needed if we editted "running" directly.
            print("Successfully updated candidate-config")
            conn.commit()
            print("Changes committed from candidate-config to running-config")
        else:
            # Something went wrong, print any errors. In a real environment,
            # there might have been valid configuration applied already,
            # so discarding any pending changes might be a safe approach.
            print("Failed to apply candidate-config")
            print(f" RPC edit-config() error: --> {config_resp.error}")
            print(f" RPC validate() error:    --> {val_resp.error}")
            conn.discard_changes()
            print("Changes discarded from candidate-config")

    return config_resp


def save_config_nxos(conn):
    """
    Save config on Cisco NX-OS is complex and requires a custom RPC.
    Reference the NX-OS programmability documentation for further details.
    """

    save_xmlns = "http://cisco.com/ns/yang/cisco-nx-os-device"
    save_rpc = f"""
        <copy_running_config_src xmlns="{save_xmlns}">
             <startup-config/>
        </copy_running_config_src>
    """
    save_resp = conn.dispatch(fromstring(save_rpc))
    return save_resp


if __name__ == "__main__":
    main()
