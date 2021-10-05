#!/usr/bin/env python


"""
Author: Nick Russo
Purpose: Using RESTCONF with IOS-XE specific YANG models to manage DHCP
server pools on a Cisco IOS-XE router via the always-on Cisco DevNet sandbox.
"""

import requests


def main():
    """
    Execution begins here.
    """

    # The IOS-XE sandbox uses a self-signed cert at present, so let's
    # ignore any obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/site/ios-xe
    api_path = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf"

    # Create 2-tuple for "basic" authentication using Cisco DevNet credentials.
    # No fancy tokens needed to get basic RESTCONF working on Cisco IOS-XE.
    auth = ("developer", "C1sco12345")

    # Define headers for issuing HTTP GET requests to receive YANG data as JSON.
    get_headers = {"Accept": "application/yang-data+json"}

    # Issue a GET request to collect the DHCP pool information only. This will
    # return a list of dictionaries where each dictionary represents a pool.
    get_pools_resp = requests.get(
        f"{api_path}/data/Cisco-IOS-XE-native:native/ip/dhcp/pool",
        headers=get_headers,
        auth=auth,
        verify=False,
    )

    # If the request succeed with a 200 "OK" message and there is
    # some text defined, then step through the JSON and extract the useful
    # bits of information.
    if get_pools_resp.status_code == 200 and get_pools_resp.text:

        # Uncomment the line below to see the JSON response; great for learning
        # import json; print(json.dumps(get_pools_resp.json(), indent=2))

        # Parse JSON from body and iterate over dicts in list
        pools = get_pools_resp.json()["Cisco-IOS-XE-dhcp:pool"]
        for pool in pools:
            net = pool["network"]["primary-network"]
            print(f"ID: {pool['id']}")
            print(f"  Domain: {pool['domain-name']}")
            print(f"  Network: {net['number']}")
            print(f"  Netmask: {net['mask']}")
            print(f"  Default gateways:")
            for defgate in pool["default-router"]["default-router-list"]:
                print(f"    {defgate}")
            print(f"  DNS servers:")
            for dns in pool["dns-server"]["dns-server-list"]:
                print(f"    {dns}")
    else:
        # Response had no body, saw error (e.g. 400), or no content (204)
        print("No DHCP pools currently configured")


if __name__ == "__main__":
    main()
