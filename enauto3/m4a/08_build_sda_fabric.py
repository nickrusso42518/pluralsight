#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Add an SDA fabric-site and assign IP pools to the
default virtual-network.
"""

import json
import time
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

    # Issue an HTTP POST request to create the fabric site
    # API appears synchronous, but also has task/execution IDs!
    print("Adding fabric site")
    fab_resp = dnac.req(
        "dna/intent/api/v1/business/sda/fabric-site",
        method="post",
        jsonbody={"siteNameHierarchy": "Global/Maryland/secretlab"},
    )
    dnac.wait_for_sda(fab_resp)

    # Issue an HTTP POST request to create the authc profile
    print("Adding authentication profile")
    auth_body = [
        {
            "siteNameHierarchy": "Global/Maryland/secretlab",
            "authenticateTemplateName": "No Authentication",
        }
    ]
    auth_resp = dnac.req(
        "dna/intent/api/v1/business/sda/authentication-profile",
        method="post",
        jsonbody=auth_body,
    )
    dnac.wait_for_sda(auth_resp)

    # Issue an HTTP POST request to assign VN to fabric site
    print("Assigning VN to fabric site")
    vn_body = [
        {
            "siteNameHierarchy": "Global/Maryland/secretlab",
            "virtualNetworkName": "DEFAULT_VN",
        }
    ]
    vn_resp = dnac.req(
        "dna/intent/api/v1/business/sda/virtual-network",
        method="post",
        jsonbody=vn_body,
    )
    dnac.wait_for_sda(vn_resp)

    # Loop over data and voice pools, and load them from disk
    for pool in ["vn_voice", "vn_data"]:
        with open(f"input_data/{pool}.json", "r") as handle:
            pool_body = json.load(handle)

        # Issue an HTTP POST request to assign pools to VN
        # Note: URL no longer has a hyphen!!!
        print(f"Assigning {pool} pool to VN")

        # For some reason, VN/pool steps are very slow, and there
        # does not appear to be a clear signal to continue. Just wait!
        time.sleep(10)
        pool_resp = dnac.req(
            "dna/intent/api/v1/business/sda/virtualnetwork/ippool",
            method="post",
            jsonbody=pool_body,
        )
        dnac.wait_for_sda(pool_resp)


if __name__ == "__main__":
    main()
