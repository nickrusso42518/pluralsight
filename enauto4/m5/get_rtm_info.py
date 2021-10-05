#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and test its Real-time Monitoring API methods.
"""

from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # First, collect all cloud vEdges by extracting the "data" value
    resp = sdwan.get_device_vedges(model="vedge-cloud")
    data_list = resp.json()["data"]

    # Run the real-time monitoring checks on sync'ed vEdges
    for vedge in data_list:
        if vedge.get("configStatusMessage", "").lower() == "in sync":
            vedge_id = vedge["system-ip"]
            print(f"Starting  vEdge {vedge_id} collection")

            # Collect the tunnel statistics. This will list
            # the tunnels to all other vEdges and their performance data
            tunnel = sdwan.get_device_tunnel_statistics(vedge_id)
            print(" Tunnel statistics")
            for item in tunnel.json()["data"]:
                print(
                    f"  pkts tx/rx: {item['tx_pkts']}/{item['rx_pkts']}"
                    f"  proto: {item['tunnel-protocol']} to {item['dest-ip']}"
                )

            # Collect the control connection details. This will list
            # connections to vManage and vSmart, and their status
            control = sdwan.get_device_control_connections(vedge_id)
            print(" Control connections")
            for item in control.json()["data"]:
                print(
                    f"  type: {item['peer-type']} proto: {item['protocol']}"
                    f"  ip: {item['public-ip']} state: {item['state']}"
                )

            print(f"Completed vEdge {vedge_id} collection")

if __name__ == "__main__":
    main()
