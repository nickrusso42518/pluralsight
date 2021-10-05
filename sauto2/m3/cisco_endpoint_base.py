#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Abstract base class to encompass common logic for all
Cisco endpoint security products.
"""

import os
import requests


class CiscoEndpointBase:
    """
    Abstract base class for Cisco endpoint security products.
    """

    def __init__(self, base_url):
        """
        Contains common logic when creating objects for any Cisco
        security product. The "base_url" is a string representing the
        first half of any request as individual resources can be
        appended for each request.
        """

        # Retain the base URL and create a new, long-lived HTTP session
        self.base_url = base_url
        self.sess = requests.session()

        # Generally common headers can be re-used over and over.
        # Content-Type not supplied because it isn't always JSON, and
        # just by setting the "json" kwarg, requests sets the Content-Type.
        self.headers = {"Accept": "application/json"}

    def base_req(self, resource, method="get", **kwargs):
        """
        Describes the basic process to issue an HTTP request to a given
        resource. The default method is "get" and the keyword arguments
        are processed by the well-known request() method.
        """

        # Issue the generic HTTP request using the object's session attribute
        resp = self.sess.request(
            url=f"{self.base_url}/{resource}",
            method=method,
            headers=self.headers,
            **kwargs,
        )

        # If any errors occurred (status code >= 400), raise an HTTPError
        resp.raise_for_status()

        # No errors occurred; return the entire response object
        return resp

    def req(self, resource, **kwargs):
        """
        Abstract method that children must implement. Will generally rely on
        base_req() for the core logic with some additional input/output
        processing as required for each product.
        """

        raise NotImplementedError("Abstract method that children must implement")

    @staticmethod
    def load_env_vars(*args):
        """
        Class-level method that is used for loading arbitrary environment
        variables by name. Returns a list of equal length to *args
        with the values of each environment variable. If a specific
        environment variable is not defined, the method raises a
        ValueError.
        """

        # Iterate over each argument representing an env var name
        ev_list = []
        for ev_name in args:

            # Try to load the vlaue of the env var
            ev_value = os.environ.get(ev_name)

            # Env var not defined; raise error and quit processing
            if not ev_value:
                raise ValueError(f"env var {ev_name} not defined")

            # Env var defined; append value to new list
            ev_list.append(ev_value)

        # Return list of env var values
        return ev_list
