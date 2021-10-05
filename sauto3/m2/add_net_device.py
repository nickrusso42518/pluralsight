#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Identity Services Engine (ISE)
REST API using the public Cisco DevNet sandbox (requires reservation).
Creates a new generic network device (802.1x authenticators) so we
can stream RADIUS failures later.
"""

import json
import requests


def main():
    """
    Execution begins here.
    """

    # The ISE sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. See here for more details:
    # https://developer.cisco.com/docs/identity-services-engine
    # You can access the API documentation at URL /ers/sdk#_
    api_path = "https://10.10.20.70:9060/ers"
    auth = ("admin", "C1sco12345!")

    # Headers are consistent for GET and POST requests
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Load in the network device from the JSON file to add
    with open("net_device.json", "r") as handle:
        net_device = json.load(handle)

    # Issue HTTP POST request with the new network device dict as body
    add_netdev = requests.post(
        f"{api_path}/config/networkdevice",
        headers=headers,
        auth=auth,
        json={"NetworkDevice": net_device},
        verify=False,
    )

    # If status_code >= 400, raise error to signal failure
    add_netdev.raise_for_status()

    # Response from POST is empty; have to get UUID by checking "Location"
    # response header for follow-on GET requests
    get_netdev = requests.get(
        add_netdev.headers["Location"], headers=headers, auth=auth, verify=False
    )
    get_netdev.raise_for_status()

    # Just write the JSON response to the console for quick verification
    print(json.dumps(get_netdev.json(), indent=2))


if __name__ == "__main__":
    main()
