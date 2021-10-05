#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to adjust minor configuration
on cameras, such as quality and retention settings.
"""

import json
from meraki_helpers import req


def main():
    """
    Execution begins here.
    """

    # Load the camera settings from JSON file
    with open("qr_settings.json", "r") as handle:
        settings = json.load(handle)

    # Iterate over the cameras collected
    for sn, body in settings.items():

        # Collect the current settings
        url = f"devices/{sn}/camera/qualityAndRetentionSettings"
        current = req(url).json()

        # Print the current quality and retention settings
        print(f"\nCurrent settings for camera {sn}")
        print(json.dumps(current, indent=2))

        # Issue a PUT request to update the settings based on the
        # JSON data read from the input file
        updated = req(url, method="put", jsonbody=body).json()

        # Print the newly updated quality and retention settings
        print(f"\nUpdated settings for camera {sn}")
        print(json.dumps(updated, indent=2))


if __name__ == "__main__":
    main()
