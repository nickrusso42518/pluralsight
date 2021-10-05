#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Watch traffic to Google DNS servers by creating new watchlist
domain entries. This will generate alerts when matching traffic is seen.
"""

from cisco_sw_cloud import CiscoSWCloud


def main():
    """
    Execution starts here.
    """

    # Create new SWC object from environment variables
    swc = CiscoSWCloud.build_from_env_vars()

    # Assemble the generic parameters for each watchlist domain
    body = {
        "reason": "Unauthorized DNS server for Globomantics",
        "category": "domain",
        "list_on": "blacklist",
        "is_bidirectional": False,
    }

    # Identify Google DNS IP addresses to watch
    watchlist_domains = [
        {"title": "Google primary DNS", "identifier": "8.8.8.8"},
        {"title": "Google alternate DNS", "identifier": "8.8.4.4"},
    ]

    # Iterate over the watchlist domains of interest
    for watchlist_domain in watchlist_domains:

        # Update the base body with the specific watchlist. This is
        # safe because the title/identifier keys are updated each time
        body.update(watchlist_domain)

        # Create each watchlist domain based on the specific JSON body
        resp = swc.req("watchlist/domains/", method="post", json=body)

        # Print status message to indicate success
        print(f"Watching {resp['identifier']} starting {resp['started_on']}")


if __name__ == "__main__":
    main()
