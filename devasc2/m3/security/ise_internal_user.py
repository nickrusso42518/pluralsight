#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Identity Services Engine (ISE).
REST API using the public Cisco DevNet sandbox (requires reservation).
"""

import requests


def main():
    """
    Execution begins here.
    """

    # The ISE sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/docs/identity-services-engine
    # You can access the API documentation at URL /ers/sdk
    api_path = "https://10.10.20.70:9060/ers"
    auth = ("admin", "C1sco12345!")

    # Headers are consistent for GET and POST requests
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Define a new user with a variety of basic parameters
    new_user = {
        "InternalUser": {
            "name": "ers_user",
            "description": "Added by ERS API using Python",
            "enabled": True,
            "changePassword": False,
            "password": "secreT123!",
        }
    }

    # Issue HTTP POST request with the new user dict as the message body
    post_resp = requests.post(
        f"{api_path}/config/internaluser",
        headers=headers,
        auth=auth,
        json=new_user,
        verify=False,
    )

    # Print appropriate message based on HTTP status code
    if post_resp.status_code == 201:
        print(f"Added new {new_user['InternalUser']['name']} user")
    else:
        print(f"New user {new_user['InternalUser']['name']} not added.")
        print(f"Status: {post_resp.status_code}   Reason: {post_resp.reason}")

    # Perform an HTTP GET to collect the list of users, which should
    # include the recently added user
    get_resp = requests.get(
        f"{api_path}/config/internaluser",
        headers=headers,
        auth=auth,
        verify=False,
    )

    # Iterate over users and print out the ID, name, and description
    for user in get_resp.json()["SearchResult"]["resources"]:
        print(
            f"ID: {user['id']}  Name: {user['name']}  Desc: {user['description']}"
        )


if __name__ == "__main__":
    main()
