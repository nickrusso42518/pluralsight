#!/usr/bin/env python


"""
Author: Nick Russo
Purpose: Using RESTCONF with IOS-XE specific YANG models to delete static
routes on a Cisco IOS-XE router via the always-on Cisco DevNet sandbox.
"""

import urllib.parse
import yaml
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

    # Read YAML declarative state with list of static routes to delete
    with open("config_state.yml", "r") as handle:
        config_state = yaml.safe_load(handle)

    # Headers for issuing HTTP DELETE requests to receive YANG data as JSON
    delete_headers = {
        "Accept": "application/yang-data+json, application/yang-data.errors+json"
    }

    # Define the URL for accessing the IPv4 static routes
    static_route_url = (
        f"{api_path}/data/ietf-routing:routing/routing-instance=default/"
        "routing-protocols/routing-protocol=static,1/static-routes/ipv4"
    )

    # Iteratively delete each route
    for route in config_state["route"]:

        # Need to ensure the prefix string is properly encoded as
        # a URL since it contains a "/" character
        prefix = route["destination-prefix"]
        enc_prefix = urllib.parse.quote(prefix, safe="")

        # Issue route-specific delete request by specifying the prefix
        delete_rte_resp = requests.delete(
            f"{static_route_url}/route={enc_prefix}",
            headers=delete_headers,
            auth=auth,
            verify=False,
        )

        # Good: 204 NO CONTENT means the route was deleted
        # Bad: 404 NOT FOUND means the route is already absent
        # Ugly: Other unexpected messages like 401, 409, etc
        if delete_rte_resp.status_code == 204:
            print(f"Prefix '{prefix}' successfully deleted")
        elif delete_rte_resp.status_code == 404:
            print(f"Prefix '{prefix}' not found; already absent")
        else:
            print(f"Prefix '{prefix}' unexpected {delete_rte_resp.status_code}")


if __name__ == "__main__":
    main()
