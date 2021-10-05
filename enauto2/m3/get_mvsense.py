#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to examine MV sense analytics.
"""

import json
import sys
from meraki_helpers import req


def main(sn):
    """
    Execution begins here.
    """

    # Query the following URL endpoints:
    #  live: exact point in time
    #  recent: past 1 minute
    #  overview: past 1 hour
    for resource in ["live", "recent", "overview"]:

        # Issue the HTTP GET request
        analytics = req(f"devices/{sn}/camera/analytics/{resource}").json()

        # Print the analytics output
        print(f"\nMV sense {resource} analytics for camera {sn}")
        print(json.dumps(analytics, indent=2))


if __name__ == "__main__":
    # Serial number must be supplied as CLI argument
    if len(sys.argv) != 2:
        print("usage: python mvsense.py <camera_serial>")
        sys.exit(1)

    # Pass in the arguments into main()
    main(sys.argv[1])
