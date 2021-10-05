#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using RESTCONF with IOS-XE specific YANG models to add static
routes on a Cisco IOS-XE router via the always-on Cisco DevNet sandbox.
"""

import requests
import yaml


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

    # Read YAML declarative state with list of static routes to add
    with open("config_state.yml", "r") as handle:
        config_state = yaml.safe_load(handle)

    # Define headers for issuing HTTP POST requests to carry JSON data
    post_headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }

    # Issue a POST request to add new static routes. This will
    # return a list of dictionaries where each dictionary represents a route.
    static_route_add_url = (
        f"{api_path}/data/ietf-routing:routing/routing-instance=default/"
        "routing-protocols/routing-protocol=static,1/static-routes/ipv4"
    )

    add_rte_resp = requests.post(
        static_route_add_url,
        headers=post_headers,
        auth=auth,
        json=config_state,
        verify=False,
    )

    # Good: 201 CREATED means routes were added
    # Bad: 409 CONFLICT means some routes already exist, cannot overwrite
    # Ugly: Other unexpected messages like 401, 404, etc
    if add_rte_resp.status_code == 201:
        print(f"Added new static routes successfully")
    elif add_rte_resp.status_code == 409:
        print(f"At least one static route already exists")
    else:
        print(f"Unexpected {add_rte_resp.status_code}")


if __name__ == "__main__":
    main()
