#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using RESTCONF with IOS-XE specific YANG models to collect static
routes on a Cisco IOS-XE router via the always-on Cisco DevNet sandbox.
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

    # Issue a GET request to collect the static routes only. This will
    # return a list of dictionaries where each dictionary represents a route.
    # The URL is broken over multiple lines for readability, and the "=" is
    # used to specify specific "keys" to query individual list elements.
    def_inst = f"{api_path}/data/ietf-routing:routing/routing-instance=default/"
    static_route_proto = "routing-protocols/routing-protocol=static,1"
    get_rte_resp = requests.get(
        def_inst + static_route_proto,
        headers=get_headers,
        auth=auth,
        verify=False,
    )

    # Uncomment the line below to see the JSON response; great for learning
    # import json; print(json.dumps(get_rte_resp.json(), indent=2))

    # Print route details in a human-readable format
    rtes = get_rte_resp.json()["ietf-routing:routing-protocol"]["static-routes"]
    for rte in rtes["ietf-ipv4-unicast-routing:ipv4"]["route"]:
        # Don't need .get() for the prefix, it's the "key"
        print(f"Prefix: {rte['destination-prefix']} via ", end="")

        # Next-hop is outgoing interface, IP address, or possibly both
        nexthop = rte["next-hop"]
        print(f"{nexthop.get('outgoing-interface', '')}", end="")
        print(f"{nexthop.get('next-hop-address', '')}")


if __name__ == "__main__":
    main()
