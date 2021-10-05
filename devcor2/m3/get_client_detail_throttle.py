#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get the current
details about specific clients by MAC address via CLI arguments.
Exits with code 1 with improper CLI usage and code 2 if any
HTTP request fails.
"""

import json
import re
import sys
import time
import requests
from tqdm import tqdm
from auth_token import get_token


# Cisco public DNAC sandbox only allows 5 requests per minute. This
# constant can be changed if the number increases
REQS_PER_MIN = 5


def main(argv):
    """
    Execution begins here.
    """

    # Reuse the get_token() function from before. If it fails
    # allow exception to crash program
    # https://developer.cisco.com/docs/dna-center-api-1210/
    host = "sandboxdnac2.cisco.com"
    token = get_token(host)

    # Declare useful local variables to simplify request process
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}

    # API requires specifying the epoch as query parameter. Take current
    # time in epoch seconds, convert to ms, and remove decimal
    # Note: epoch 0 = 00:00:00 UTC on 1 January 1970
    current_epoch = int(time.time() * 1000)
    params = {"timestamp": current_epoch}

    # Pass CLI arguments into processor function to return subset of
    # valid, correctly formatted MAC addresses (error checking)
    macs = get_macs(argv)

    # Iterate over all valid MAC addresses
    for i, mac in enumerate(macs):
        # Add a new key to specify the MAC address to query
        params["macAddress"] = mac

        # Issue HTTP GET request to get specific client details
        get_resp = requests.get(
            f"https://{host}/dna/intent/api/v1/client-detail",
            headers=headers,
            params=params,
        )

        # Print error details (rather than raise error) and exit if failure
        get_resp_json = get_resp.json()
        if not get_resp.ok:
            print(f"Request failed: {get_resp.status_code}/{get_resp.reason}")
            print(json.dumps(get_resp_json, indent=2))
            sys.exit(2)

        # Print JSON response for troubleshooting and learning
        # print(json.dumps(get_resp_json, indent=2))

        # Request succeeded; print
        stats = get_resp_json["detail"]
        print(f"Wireless details for MAC {mac}")
        print(f"  IPv4 Address: {stats['hostIpV4']}")
        print(f"  Freq/chan: {stats['frequency']} GHz / {stats['channel']}")
        print(f"  RSSI/SNR: {stats['rssi']} / {stats['snr']}\n")

        # API will return 429 (too many requests) if we send more than
        # 5 per minute. After every 5th request, just wait 58 seconds
        # and use a progress bar for visual aid.
        if (i + 1) % REQS_PER_MIN == 0:
            print("*** Sleeping for 1 minute to avoid API throttle ***")
            for _ in tqdm(range(60)):
                time.sleep(1)
            print()


def get_macs(argv):
    """
    Returns a list of valid MAC addresses from the CLI arguments.
    Using regular expression (regex) to validate that input is in the
    proper format, such as "00:00:2A:01:00:01" to give a specific example.
    """

    # Ensure there is at least one MAC specified. If not, print usage and exit
    if len(argv) < 2:
        print(f"usage: python {sys.argv[0]} <mac1> <mac2> ... <macN>")
        sys.exit(1)

    # Create empty list of valid MACs and hex digit regex char pattern
    macs = []
    h2 = "[0-9a-fA-F]{2}"
    regex = re.compile(f"{h2}:{h2}:{h2}:{h2}:{h2}:{h2}")

    # Check each CLI arg for a match against pattern, and add to list
    # using uppercase letters if match succeeds
    for arg in argv[1:]:
        if regex.match(arg):
            macs.append(arg.upper())

    # Return new list of valid MAC addresses
    return macs


if __name__ == "__main__":
    # Ensure main() has access to the system CLI args from the shell
    main(sys.argv)
