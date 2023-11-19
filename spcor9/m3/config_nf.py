#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using RESTCONF with IOS-XE specific YANG models to configure NetFlow
policies on a Cisco IOS-XE router.
"""

import json
import httpx

# Centralized inputs for easy modification
USERNAME = "labadmin"
PASSWORD = "labadmin"
HOST = "10.0.90.8"
PE_INTF = "GigabitEthernet=2.3078"

def main():
    """
    Execution begins here.
    """

    # Define the basic API path (sometimes called base URL)
    api_path = f"https://{HOST}:443/restconf"

    # Create 2-tuple for "basic" authentication using defined credentials.
    # No fancy tokens needed to get basic RESTCONF working on Cisco IOS-XE.
    auth = (USERNAME, PASSWORD)

    # Read declarative state with the YANG-modeled, JSON-encoded data to add
    with open("add_csr_nf.json", "r") as handle:
        netflow_data = json.load(handle)

    # Create HTTP headers to indicate YANG/JSON data being sent and received.
    post_headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }

    # Open long-lived TLS sessions to improve performance. Also, disable
    # certificate validation as routers currently use self-signed TLS certs.
    with httpx.Client(verify=False) as client:

        # Issue HTTP PUT request to modify the NetFlow config.
        netflow_add_resp = client.put(
            f"{api_path}/data/Cisco-IOS-XE-native:native/flow",
            headers=post_headers,
            auth=auth,
            json=netflow_data["main_config"],
        )

        # Raise error if request failed; otherwise, do nothing
        netflow_add_resp.raise_for_status()
        print("Added generic NetFlow configuration successfully")

        # Issue HTTP PUT request to apply the NetFlow policy.
        netflow_path = f"interface/{PE_INTF}/ip/flow"
        netflow_intf_resp = client.put(
            f"{api_path}/data/Cisco-IOS-XE-native:native/{netflow_path}",
            headers=post_headers,
            auth=auth,
            json=netflow_data["intf_apply"],
        )
        netflow_intf_resp.raise_for_status()
        print("Enabled NetFlow on target interface")

        # Save configuration to ensure the changes persist across reboots.
        save_config_resp = client.post(
            f"{api_path}/operations/cisco-ia:save-config",
            headers=post_headers,
            auth=auth,
        )

        # If successful, indicate so, or print error message
        if save_config_resp.is_success:
            print("Saved configuration successfully")
        else:
            print("Failed to save configuration")


if __name__ == "__main__":
    main()
