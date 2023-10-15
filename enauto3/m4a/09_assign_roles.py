#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Assign edge/control-plane roles and onboard a new host.
"""

import json
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    # Can use DevNet reservable instance (10.10.20.85) or dCloud HW sandbox
    # https://dcloud.cisco.com
    dnac = DNACRequester(
        # host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
        host="198.18.129.100",
        username="admin",
        password="C1sco12345",
        verify=False,
    )

    # Issue an HTTP POST request to assign c9300-3 as control-plane device
    ctlp_ip = "198.18.128.24"
    print(f"Adding control-plane device {ctlp_ip}")
    ctlp_body = {
        "deviceManagementIpAddress": ctlp_ip,
        "siteNameHierarchy": "Global/Maryland/secretlab",
    }
    ctpl_resp = dnac.req(
        "dna/intent/api/v1/business/sda/control-plane-device",
        method="post",
        jsonbody=ctlp_body,
    )
    dnac.wait_for_sda(ctpl_resp)

    # Issue HTTP POST requests to assign c9300-1/2 as edge devices
    for edge_ip in ["198.18.128.22", "198.18.128.23"]:
        print(f"Adding edge device {edge_ip}")
        edge_body = {
            "deviceManagementIpAddress": edge_ip,
            "siteNameHierarchy": "Global/Maryland/secretlab",
        }
        edge_resp = dnac.req(
            "dna/intent/api/v1/business/sda/edge-device",
            method="post",
            jsonbody=edge_body,
        )
        dnac.wait_for_sda(edge_resp)

    # Load sample onboarding data from disk
    with open("input_data/onboard1.json", "r") as handle:
        onboard_body = json.load(handle)

    # Onboard host with high timeout (very slow to respond)
    print("Onboarding sample host")
    onboard_resp = dnac.req(
        "dna/intent/api/v1/business/sda/hostonboarding/user-device",
        method="post",
        jsonbody=onboard_body,
        timeout_sec=30,
    )
    dnac.wait_for_sda(onboard_resp)


if __name__ == "__main__":
    main()
