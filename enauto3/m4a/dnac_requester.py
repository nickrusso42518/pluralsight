#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Contains a helper class to make issuing DNAC REST API
requests simpler.
"""

import time
import requests


class DNACRequester:
    """
    Lightweight SDK class to simplify interacting with the DNAC REST API.
    """

    def __init__(self, host, username, password, verify=True, old_style=False):
        """
        Constructor to build a new object. Automatically collects an
        authorization token and assembles the headers used for all
        future requests.
        """

        # Store the host and verify parameters for use later
        self.host = host
        self.verify = verify

        # If verify is false, we should disable unnecessary SSL logging
        if not verify:
            requests.packages.urllib3.disable_warnings()

        # Build common headers
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Get token, then update headers dict
        if old_style:
            auth_url = "api/system/v1/auth/token"
        else:
            auth_url = "dna/system/api/v1/auth/token"

        auth_resp = self.req(auth_url, method="post", auth=(username, password))
        auth_resp.raise_for_status()
        self.headers["X-Auth-Token"] = auth_resp.json()["Token"]

    def req(
        self,
        resource,
        method="get",
        auth=None,
        jsonbody=None,
        params=None,
        raise_for_status=True,
        timeout_sec=5,
    ):
        """
        Issues a generic request. Basically, a wrapper for "requests" using
        the already-stored host, headers, and verify parameters.
        """
        resp = requests.request(
            method=method,
            url=f"https://{self.host}/{resource}",
            auth=auth,
            headers=self.headers,
            json=jsonbody,
            params=params,
            verify=self.verify,
            timeout=timeout_sec,
        )

        # Debugging statement to explore the response body structure
        # import json; print(json.dumps(resp.json(), indent=2))

        # Raise HTTPError if status_code >= 400, otherwise return resp object
        if raise_for_status:
            resp.raise_for_status()
        return resp

    def wait_for_task(self, task_id, wait_time=5, attempts=3):
        """
        Waits the wait_time times the number of attempts for the specified
        task_id to be complete. Raises ValueError if the task fails or
        TimeoutError if it fails to complete in the required timeframe.
        """
        for _ in range(attempts):
            time.sleep(wait_time)

            # Query DNA center for the status of the specific task ID
            task_resp = self.req(f"dna/intent/api/v1/task/{task_id}")
            task_data = task_resp.json()["response"]

            # If an error occurred, fail immediately. The failure reason is
            # often defined, but if not, use the progress string
            if task_data["isError"]:
                reason = task_data.get("failureReason", task_data["progress"])
                raise ValueError(f"Async task error: {reason}")

            # isError is false, but we might not be done yet. Check for
            # the "endTime" key. If present, we are done
            if "endTime" in task_data:
                return task_resp

            # isError is false but we are not done. Keep looping

        # Loop terminated; task did not complete in time
        total = wait_time * attempts
        raise TimeoutError(f"Task timed out in {total} seconds")

    def wait_for_exec_status(self, status_url, wait_time=5):
        """
        This API is asynchronous and uses HTTP status 202, but does not use the
        same "task ID" query process as most other DNA Center tasks. Use a
        while loop to wait forever until success or failure (for variety).
        """

        # Continue looping until explicitly exited
        while True:
            time.sleep(wait_time)

            # After waiting, send request and see if the task is in progress
            status_resp = self.req(status_url)
            status_data = status_resp.json()

            # If an error occurred, fail immediately
            if status_data["status"].lower().startswith("fail"):
                raise ValueError(f"Exec status: {status_data['bapiError']}")

            # If success, return the status response
            if status_data["status"].lower() == "success":
                return status_resp

            # Neither failure nor success; still in progress, loop again
