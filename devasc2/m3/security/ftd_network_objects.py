#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Firepower Threat Defense (FTD)
REST API using the public Cisco DevNet sandbox (requires reservation).
"""

import requests


def main():
    """
    Execution begins here.
    """

    # The FTD sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/firepower/
    api_path = "https://10.10.20.65/api/fdm/v2"

    # To authenticate, we issue a POST request with our username/password
    # as a JSON body to obtain a bearer token in response.
    post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # This is the JSON payload included in the initial POST request to
    # obtain a bearer token.
    token_data = {
        "grant_type": "password",
        "username": "admin",
        "password": "Cisco1234",
    }

    # Issue the POST request to the proper URL with the predefined headers
    # and body dictionaries. Be sure to ignore SSL cert checking as this
    # is a standalone sandbox FTD instance.
    token_response = requests.post(
        f"{api_path}/fdm/token",
        headers=post_headers,
        json=token_data,
        verify=False,
    )

    # We've obtained the bearer token, so store it in a local
    # variable for easy reference. Then, create
    bearer_token = token_response.json()["access_token"]
    # print(f"token is: {bearer_token}")

    # Update the GET and POST header dictionaries with this new bearer
    # token so future requests will authenticate correctly.
    auth_headers = {"Authorization": f"Bearer {bearer_token}"}
    get_headers = {"Accept": "application/json"}
    get_headers.update(auth_headers)
    post_headers.update(auth_headers)

    # Issue a GET request to collect a list of network objects configured
    # on FTD. These are the IP subnets, hosts, and FQDNs that might be
    # included in various security access policies.
    get_net_response = requests.get(
        f"{api_path}/object/networks", headers=get_headers, verify=False
    )

    # Iterate over the list of networks and print out a few of the
    # most interesting values such as name, ID, and prefix/FQDN value.
    for net in get_net_response.json()["items"]:
        print(f"Name: {net['name']}  ID: {net['id']}  Value: {net['value']}")

    # Add a new network, much like the DevNet example. I'm adding my own
    # website as an FQDN just as a silly example. This dict represents the
    # JSON body of the POST request which adds the network object.
    website_fqdn = {
        "name": "Nick_Web",
        "description": "Nick Russo website",
        "subType": "FQDN",
        "value": "njrusmc.net",
        "type": "networkobject",
    }

    # Issue the POST request with the dict defined above.
    post_net_response = requests.post(
        f"{api_path}/object/networks",
        headers=post_headers,
        json=website_fqdn,
        verify=False,
    )

    # If the object already exists, the request will receive a 422
    # response indicating that the object already exists. A more elegant
    # approach would be checking for existing before issuing the POST,
    # but this is just a simple example.
    if post_net_response.ok:
        print("Added njrusmc.net object for the first time")


if __name__ == "__main__":
    main()
