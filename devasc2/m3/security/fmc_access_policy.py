#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Firepower Management Console (FMC)
REST API using the public Cisco DevNet sandbox (requires reservation).
"""

import requests


def main():
    """
    Execution begins here.
    """

    # The FMC sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. See here for more details:
    # https://developer.cisco.com/firepower/
    api_path = "https://fmcrestapisandbox.cisco.com/api"

    # Issue the POST request to the proper URL with the predefined headers
    # and body dictionaries. Be sure to ignore SSL cert checking as this
    # FMC doesn't have production certs. Use HTTP basic auth with your
    # specific username and password from the DevNet reservation system.
    basic_auth = ("YOUR_USERNAME", "YOUR_PASSWORD")

    # Issue a POST request using the basic auth parameters to get an auth
    # token in response for all future API calls. It also returns a list of
    # domain UUIDs for which the user is authenticated, but in this example,
    # there is only one, which is the "global" domain.
    token_response = requests.post(
        f"{api_path}/fmc_platform/v1/auth/generatetoken",
        auth=basic_auth,
        verify=False,
    )
    token = token_response.headers["X-auth-access-token"]
    domain_uuid = token_response.headers["DOMAIN_UUID"]

    # Assemble the GET headers to accept JSON data back and to use the auth
    # token generated earlier.
    get_headers = {"Accept": "application/json", "X-auth-access-token": token}

    # The default limit appears to be 25, so increse to 100 if the FMC has
    # many test policies on it. The expanded details are false by default,
    # but you can change this to true to easily get more policy information.
    policy_params = {"limit": 100, "expanded": False}

    # Issue the GET request using the proper headers and parameters defined
    # above. This collects a list of all FMC access policies.
    get_policy_response = requests.get(
        f"{api_path}/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies",
        headers=get_headers,
        params=policy_params,
        verify=False,
    )

    # Iterate over all the access policies and print the ID and name
    # for each one to ensure they were collected successfully.
    for policy in get_policy_response.json()["items"]:
        print(f"ID: {policy['id']}  Name: {policy['name']}")

    # Define a new policy to add with a minimum of information.
    new_policy = {
        "type": "AccessPolicy",
        "name": "Nick was here",
        "defaultAction": {"action": "BLOCK"},
    }

    # Define the POST headers which also adds the Content-Type header.
    post_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-auth-access-token": token,
    }

    # Issue a POST request against the same URL except passing in the
    # JSON body (as a string) to add the new policy.
    add_policy_response = requests.post(
        f"{api_path}/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies",
        headers=post_headers,
        json=new_policy,
        verify=False,
    )

    # If the object already exists, the request will receive a 400
    # response indicating that the object already exists. A more elegant
    # approach would be checking for existing before issuing the POST,
    # but this is just a simple example.
    if add_policy_response.ok:
        print("Added new access policy successfully")


if __name__ == "__main__":
    main()
