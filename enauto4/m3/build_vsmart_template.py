#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
add a new vSmart device template.
"""

from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # Build a simple vSmart device template based off
    # factory-default feature templates required
    temp_resp = sdwan.add_fd_vsmart_device_template()

    # Extract the template ID and define the variables needed
    # to attach the template. Each kv-pair maps to a vSmart instance.
    template_id = temp_resp.json()["templateId"]
    var_map = {"vsmart-01": ("100", "10.10.20.254")}
    print(f"Added vSmart template (factory-defaults) with ID {template_id}")

    # Attach the template to the vSmarts (async) and wait for completion
    attach_resp = sdwan.attach_vsmart_device_template(template_id, var_map)
    data = attach_resp.json()["summary"]
    print(f"vSmart template attachment status: {data['status']}")
    print(f"Result counts: {data['count']}")


if __name__ == "__main__":
    main()
