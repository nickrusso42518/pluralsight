#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to delete an existing
device from Cisco DNA Center using the REST API.
"""

import time
import requests
from auth_token import get_token


def main():
    """
    Execution begins here.
    """

    # Reuse the get_token() function from before. If it fails
    # allow exception to crash program
    token = get_token()

    # Declare useful local variables to simplify request process
    api_path = "https://sandboxdnac.cisco.com/dna"
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}

    # Issue an HTTP GET to search for a specific device by IP address
    delete_ip = "192.0.2.1"
    get_resp = requests.get(
        f"{api_path}/intent/api/v1/network-device/ip-address/{delete_ip}",
        headers=headers,
    )

    # If the device was found, continue with deletion
    if get_resp.ok:
        delete_id = get_resp.json()["response"]["id"]
        print(f"Found device with mgmt IP {delete_ip} and ID {delete_id}")

        # Issue HTTP DELETE and specify the device ID. Like the HTTP POST
        # to add a device, this is an asynchronous operation
        delete_resp = requests.delete(
            f"{api_path}/intent/api/v1/network-device/{delete_id}",
            headers=headers,
        )

        # If delete succeeded, check task ID for completion
        if delete_resp.ok:

            # Wait 10 seconds after server responds
            print(f"Request accepted: status code {delete_resp.status_code}")
            time.sleep(10)

            # Query DNA center for the status of the specific task ID
            task = delete_resp.json()["response"]["taskId"]
            task_resp = requests.get(
                f"{api_path}/intent/api/v1/task/{task}", headers=headers
            )

            # See if the task was completed successfully or not
            if task_resp.ok:
                task_data = task_resp.json()["response"]
                if not task_data["isError"]:
                    print("Old device successfully deleted")
                else:
                    print(f"Async task error seen: {task_data['progress']}")
            else:
                print(f"Async GET failed: status code {task_resp.status_code}")

        else:
            # The initial HTTP DELETE failed; print details
            print(f"Device removal failed with code {delete_resp.status_code}")
            print(f"Failure body: {delete_resp.text}")

    else:
        print(f"Could not find device with mgmt IP {delete_ip}")
        print(f"Code: {get_resp.status_code}  Body: {get_resp.text}")


if __name__ == "__main__":
    main()
