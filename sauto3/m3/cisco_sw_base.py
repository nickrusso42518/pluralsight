#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Abstract base class to encompass common logic for all
Cisco Stealthwatch security products.
"""

import requests


class CiscoSWBase:
    """
    Abstract base class for Cisco Stealthwatch security products.
    """

    def __init__(self, host, verify=True):
        """
        Contains common logic when creating objects for any Cisco
        security product. The "host" is a string representing the
        host to connect to, but the base URLs will be product-specific.
        """

        # Retain supplied host and create a new, long-lived HTTP session
        self.host = host
        self.sess = requests.session()

        # If verify is false, we should also disable SSL warnings (sandbox)
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Sometimes common headers can be re-used over and over.
        # Content-Type not supplied because it isn't always JSON, and
        # just by setting the "json" kwarg, requests sets the Content-Type.
        self.headers = {"Accept": "application/json"}

    def req(self, resource, method="get", **kwargs):
        """
        Issues a generic HTTP request to a given resource and with given
        keyword arguments. Returns the body of the response, if it exists,
        as Python objects.
        """

        # If headers were not supplied, use the default headers. Some
        # requests have different headers (weird), so we cannot use
        # them all the time
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers

        # Issue the generic HTTP request using the object's session attribute
        resp = self.sess.request(
            url=f"{self.base_url}/{resource}",
            method=method,
            verify=self.verify,
            **kwargs,
        )

        # If any errors occurred (status code >= 400), raise an HTTPError
        resp.raise_for_status()

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            # import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}
