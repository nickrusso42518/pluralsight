#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Creates an interface for Cisco ISE PxGrid to include
control REST API, service REST API, and websocket subscription activity.
"""

import time
import requests


class PxGrid:
    """
    Represents an interaction to PxGrid for REST and websocket services.
    """

    def __init__(self, ise_host, verify=False):
        """
        Creates a new object to a specific ISE host (IP or hostname) and
        whether SSL certifications should be verified or not.
        """

        # If verify is false, we should also disable SSL warnings (sandbox)
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a long-lived TCP session for HTTP requests, plus base URL
        self.sess = requests.session()
        self.control_url = f"https://{ise_host}:8910/pxgrid/control"
        self.control_auth = None

        # Define generic send/receive JSON headers for HTTP/REST
        self.http_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    #
    # Generic helper methods
    #

    def _base_req(self, resource, base_url, method="post", **kwargs):
        """
        Internal-only helper for issuing generic HTTP requests with a
        specific base_url. All requests are POST requests, but the method
        can be overriden if this changes in the future.
        """

        # All requests must have a JSON body, so if this wasn't
        # supplied, use an empty dict instead
        if "json" not in kwargs:
            kwargs["json"] = {}

        # Issue generic HTTP request by combining relatively fixed
        # object attributes with arguments from caller
        resp = self.sess.request(
            url=f"{base_url}/{resource}",
            method=method,
            headers=self.http_headers,
            verify=self.verify,
            **kwargs,
        )
        resp.raise_for_status()

        # If the response has an HTTP body, return Python objects from it
        if resp.text:
            # Optional debugging line to see the HTTP responses
            # import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # No body; just return empty dict for consistency
        return {}

    def service_req(self, resource, **kwargs):
        """
        Perform a service request based on the specific resource specified,
        along with any additional keyword arguments.
        """
        return self._base_req(
            resource,
            base_url=self.service_url,
            auth=self.service_auth,
            **kwargs,
        )

    def control_req(self, resource, **kwargs):
        """
        Perform a control request based on the specific resource specified,
        along with any additional keyword arguments.
        """
        return self._base_req(
            resource,
            base_url=self.control_url,
            auth=self.control_auth,
            **kwargs,
        )

    def lookup_service(self, service_name):
        """
        Perform a service lookup for a specific service, such as "radius"
        or "pubsub".
        """
        resp = self.control_req("ServiceLookup", json={"name": service_name})
        return resp

    #
    # User/connection initialization
    #

    def activate_user(self, username):
        """
        Performs the general workflow to create a new pxGrid user via the
        username/password approach. The username, password, and shared secret
        are retained for use later.
          1. AccountCreate
          2. AccountActivate
        """

        # Store the username for later (used for websockets too)
        self.username = username

        # Issue a POST request to create a new account with specified username
        # This request does not require authentication
        acct = self.control_req("AccountCreate", json={"nodeName": username})

        # Build the HTTP basic auth 2-tuple for future requests
        self.control_auth = (self.username, acct["password"])

        # User creation successful; print status message
        print(f"PxGrid user {username} created. Please approve via ISE UI")

        # Loop forever (or until otherwise broken)
        while True:
            activate = self.control_req("AccountActivate")
            account_state = activate["accountState"].lower()
            print(f"Account state: {account_state}")

            # Test for different states. Enabled is good, disabled is bad
            if account_state == "enabled":
                break
            elif account_state == "disabled":
                raise ValueError(f"PxGrid user {username} disabled")

            # Docs recommend waiting 60 seconds between requests; will use
            # a smaller value to speed up testing
            time.sleep(10)

        print(f"PxGrid user {username} activated")

    def authorize_for_service(self, service):
        """
        Allows consumption of a specific service. The service lookup
        occurs first, followed by either a websocket setup or a REST
        API setup depending on 'ws_subscribe'.
        """

        # First, lookup the service name to determine two things:
        # The pubsub service, which provides the ws URL and nodename
        # The session topic, which is used for signaling interest
        serv_resp = self.lookup_service(service)["services"][0]

        # Issue POST request to generate secret between consumer (us) and
        # specific ISE node publisher
        pub_node = serv_resp["nodeName"]
        secret_resp = self.control_req(
            "AccessSecret", json={"peerNodeName": pub_node}
        )

        # Extract and store the secret text
        self.secret = secret_resp["secret"]

        # Store the ISE URL and auth for use in future service_req() calls
        self.service_auth = (self.username, self.secret)
