#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Submit sample events to Umbrella Enforcement API for processing
and print the response in a simple text format.
"""

import json
import time
from cisco_umbrella_enforcement import CiscoUmbrellaEnforcement


def main():
    """
    Execution starts here.
    """

    # Instantiate a new Umbrella Enforcement object from env vars
    umb_enf = CiscoUmbrellaEnforcement.build_from_env_vars()

    # Open the JSON file for reading; load in the sample events
    with open("sample_events.json", "r") as handle:
        body = json.load(handle)

    # Issue a POST request to the "events" resource to simulate another
    # application sending these events to Umbrella for analysis/logging
    # Response isn't useful (a malformed UUID)
    umb_enf.req("events", method="post", json=body)

    # Wait a short time for the domains to show up;
    # could introduce more advanced "waiting" logic
    time.sleep(5)

    # Get the domains seen by the enforcement API
    domains = umb_enf.req("domains")

    # Iterate over each domain and print them out in trivial
    # fashion on one line each, adding a numeric counter
    for i, entry in enumerate(domains["data"]):
        text = f"{i+1}. "

        # Unpack the k/v pairs for each entry
        for key, value in entry.items():
            text += f"{key}: {value}  "

        # Print the final result during each outer loop iteration. Example:
        # 1. id: 30916  name: internetbadguys.com  lastSeenAt: 1593198847
        # 2. id: 50213434  name: malware4less.com  lastSeenAt: 1593198847
        print(text.strip())


if __name__ == "__main__":
    main()
