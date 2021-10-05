#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to collect video
footage from MV sense cameras.
"""

import os
import sys
import time
import requests
from meraki_helpers import get_network_id, req


def main(org_name, net_name, timestamp):
    """
    Execution begins here.
    """

    # Create output directory for snapshots
    snapshot_dir = "snapshots"
    if not os.path.exists(snapshot_dir):
        os.makedirs(snapshot_dir)

    # Find the network ID for the specified org and network
    net_id = get_network_id(net_name, org_name)

    # Collect a list of cameras within this network
    cameras = req(f"networks/{net_id}/devices").json()

    # Print the list of cameras collected
    # import json; print(json.dumps(cameras, indent=2))

    # Iterate over the cameras collected
    for camera in cameras:
        sn = camera["serial"]

        # Get the live video link. Note that accessing this link requires
        # you to log into the Meraki dashboard
        video_link = req(f"networks/{net_id}/cameras/{sn}/videoLink").json()

        # Print the retrieved video link response
        # import json; print(json.dumps(video_link, indent=2))
        print(f"Video link for camera {sn}:\n{video_link['url']}")

        # If a timestamp was specified, build it into a query parameter
        # Example timestamp format: 2020-012-31T12:51:52Z
        if timestamp:
            params = {"timestamp": timestamp}
        else:
            params = None

        # Generate a new snapshot at the given timestamp, or if one isn't
        # specified, at the current time
        snapshot_link = req(
            f"networks/{net_id}/cameras/{sn}/snapshot",
            method="post",
            params=params,
        ).json()

        # Print the retrieved snapshot link response
        # import json; print(json.dumps(snapshot_link, indent=2))

        for _ in range(5):
            # It takes some time for the snapshot to be available, usually
            # 3 seconds, so wait for a short time until the process completes
            time.sleep(3)

            # Perform a low-level GET request to the snapshot URL which does not
            # use the Meraki dashboard API, nor does it require authentication.
            image = requests.get(snapshot_link["url"])

            # If HTTP code 200 (OK) is returned, quit the loop and continue
            if image.status_code == 200:
                break
        else:
            print(f"Could not collect snapshot for camera {sn} right now")
            continue

        # Open a new jpg file for writing bytes (not text) and include
        # the HTTP content as bytes (not text)
        with open(f"{snapshot_dir}/{sn}.jpg", "wb") as handle:
            handle.write(image.content)

        print(f"Snapshot for camera {sn} saved")


if __name__ == "__main__":
    # Get the org name from the env var; default to DevNet
    org = os.environ.get("MERAKI_ORG_NAME", "DevNet Sandbox")

    # Get the network name from the env var; default to DevNet
    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    # Process optional timestamp if specified
    timest = None
    if len(sys.argv) > 1:
        timest = sys.argv[1]

    # Pass in the org, network, and optional timestamp arguments into main()
    main(org, net, timest)
