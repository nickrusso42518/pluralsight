#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Cisco Intersight data collection using the DevNet
sandbox (requires reservation).
"""

import os
from operator import itemgetter
import requests
from intersight_auth import IntersightAuth


def main():
    """
    Execution begins here.
    """

    # These keys are actually important to protect, so we can use the env var
    # strategy used with Webex Teams in a previous course. Users must export
    # the 'INTERSIGHT_KEY' env var before continuing.
    api_key = os.environ.get("INTERSIGHT_KEY")
    if not api_key:
        fail_with_msg("Specify key: 'export INTERSIGHT_KEY=<key_string>'")

    privpath = os.environ.get("INTERSIGHT_SECRET_FILE")
    if not privpath:
        fail_with_msg("Specify path: 'export INTERSIGHT_SECRET_FILE=<path>'")

    # Create an auth header object using the secret key file and key ID.
    # Both are specific to your Intersight account and should be protected.
    auth = IntersightAuth(secret_key_filename=privpath, api_key_id=api_key)

    # Retrieve data about the network devices and servers in the network.
    # This should match what is available in the Intersight dashboard
    intersight_get("network/Elements", auth)
    intersight_get("compute/PhysicalSummaries", auth)


def intersight_get(resource, auth):
    """
    Helper function to collect data from specific resources and print
    subsets of that data to stdout for validation.
    """

    # Perform an HTTP get by combining the base Intersight API URL and
    # the specific source to be queried. Raise HTTPError on failure.
    api_path = "https://intersight.com/api/v1"
    get_resp = requests.get(f"{api_path}/{resource}", auth=auth)
    get_resp.raise_for_status()

    # Optionally print the JSON structure for troubleshooting/learning
    # import json; print(json.dumps(get_resp.json(), indent=2))

    # If the Results key has a None value, there is a chance that
    # there is a communication/configuration problem between Intersight
    # and the UCS managers.
    results = get_resp.json()["Results"]
    if results is None:
        print(f"No results from {resource}; is your UCS Manager claimed?")
        return

    # Sort the list of dictionaries based on "Dn" which appears to be
    # included in many responses
    items = sorted(results, key=itemgetter("Dn"))
    print(f"Collected ({len(items)}) items from {resource}")

    # Iterate over each item, printing the DN and model number
    for item in items:
        print(f"DN: {item['Dn']:<25}  Model: {item['Model']}")
    print()


def fail_with_msg(msg):
    """
    An alternative to raising errors, this function prints out the supplied
    message and exits the program with code 1.
    """
    print(msg)
    import sys
    sys.exit(1)


if __name__ == "__main__":
    main()
