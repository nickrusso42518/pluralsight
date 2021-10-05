#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simulate the Meraki cloud by spoofing test location data
using HTTP POST requests with static JSON data.
"""

import json
import requests

# Define the validator and secret, which Meraki would already know
VALIDATOR = "c8b77133f4bd2218df387186212a6e946d5b4207"
SECRET = "globo123!"


def main():
    """
    Execution begins here.
    """

    # Identify the server URL and read in JSON data before connecting
    recv_url = "https://your.domain.com:5000"
    with open("data.json", "r") as handle:
        data = json.load(handle)

    # Issue GET request to the URL that will return the validator in plain-text
    get_resp = requests.get(f"{recv_url}")
    get_resp.raise_for_status()

    # If the validator from the server matches what Meraki wants ...
    if get_resp.text == VALIDATOR:

        # Update our data dict with the shared secret and send a dummy POST
        data["secret"] = SECRET
        headers = {"Content-Type": "application/json"}
        post_resp = requests.post(f"{recv_url}", headers=headers, json=data)

        if post_resp.ok:
            # Success; reveal how many data entries were sent in summary
            tx_obs = len(data["data"]["observations"])
            rx_obs = post_resp.json()["num_observations"]

            # Sanity check; ensure sent items equals received items,
            # then print the total count
            assert tx_obs == rx_obs
            print(f"Sent and received {tx_obs} observations")

        else:
            # Failure; print status code, reason, and detailed body text
            print(f"Failed: {post_resp.status_code}/{post_resp.reason}", end="")
            print(f" - {post_resp.text}")

    else:
        # If the GET request didn't contain the correct validator, show
        # the difference so the user can correct it
        print(f"Validator mismatch; saw {get_resp.text}, expected {VALIDATOR}")


if __name__ == "__main__":
    main()
