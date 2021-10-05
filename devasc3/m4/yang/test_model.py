#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume pyangbind Python object-oriented bindings to
interact with custom YANG model. Inspired by David Barroso:
https://napalm-automation.net/yang-for-dummies/
"""

import json
import interfaces


def main():
    """
    Execution begins here.
    """
    ints = interfaces.interfaces()

    # Add Ethernet0/1, enable it, and place into VLAN 10
    eth01 = ints.interface_container.switchport_list.add("Ethernet0/1")
    eth01.enabled = True
    eth01.vlan = 10

    # Add Ethernet0/2, enable it, and place into VLAN 20
    eth02 = ints.interface_container.switchport_list.add("Ethernet0/2")
    eth02.enabled = True
    eth02.vlan = 20

    # Add Ethernet0/3, but try and set VLAN to 9999
    eth03 = ints.interface_container.switchport_list.add("Ethernet0/3")
    try:
        print("Trying to set bogus VLAN 9999")
        eth03.vlan = 9999
    except ValueError as exc:
        # This code always runs, since VLAN 9999 is never valid
        print(exc.args[0]["error-string"])

    # Add Loopback0, enable it, and set an IP address
    lb0 = ints.interface_container.virtual_list.add("Loopback0")
    lb0.enabled = True
    lb0.ip_address = "192.0.2.1"

    # Add Loopback1, but leave all default values in place
    lb1 = ints.interface_container.virtual_list.add("Loopback1")

    # Print JSON representation of the current config
    print(json.dumps(ints.get(), indent=2))


if __name__ == "__main__":
    main()
