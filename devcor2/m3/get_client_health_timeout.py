#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get the current
wired and wireless client health from Cisco DNA Center using the REST API.
"""

import time
import requests
from auth_token import get_token


# get-health timeout and number of times to attempt if timeout occurs
TIMEOUT = 10
ATTEMPTS = 3


def main():
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

    # Run the loop however many times is specified by ATTEMPTS
    for i in range(ATTEMPTS):

        # Code in the "try" block may raise errors
        try:
            # Issue HTTP GET request to get high-level client health
            get_resp = requests.get(
                f"https://{host}/dna/intent/api/v1/client-health",
                headers=headers,
                params=params,
                timeout=TIMEOUT,
            )

            # Request succeeded, break out of loop early
            if get_resp.ok:
                break

        except requests.exceptions.ReadTimeout:
            # Catch error, print message, and quit the program
            # with error code 1 if we are on the last attempt
            print(f"Timeout {i+1}/{ATTEMPTS} ({TIMEOUT} sec)")
            if i + 1 == ATTEMPTS:
                print("Could not collect client health")
                import sys
                sys.exit(1)

    # Convert HTTP response body to JSON to extract health data
    get_resp_json = get_resp.json()

    # Print JSON response for troubleshooting and learning
    # import json; print(json.dumps(get_resp_json, indent=2))

    # Iterate over all score details and categories
    for score in get_resp_json["response"]:
        for cat in score["scoreDetail"]:

            # Print the client type (wired or wireless) then the quantity
            # of clients at each quality level. Finish up with a newline
            print(f"{cat['scoreCategory']['value']} client health")
            for qual in cat["scoreList"]:
                print(f"  {qual['scoreCategory']['value']:<6}", end=" ")
                print(f"clients: {qual['clientCount']}")
            print()


if __name__ == "__main__":
    main()
