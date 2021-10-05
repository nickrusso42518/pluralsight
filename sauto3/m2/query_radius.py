#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Used to subscribe to a service using PxGrid websockets
for streaming security telemetry. Takes 1 CLI argument specifying
the service string.
"""

import sys
from pxgrid import PxGrid


def main(service):
    """
    Execution begins here.
    """

    # Instantiate a new PxGrid object to the DevNet sandbox (10.10.20.70)
    pxgrid = PxGrid("ise24.abc.inc")

    # Activate a new user for this integration
    pxgrid.activate_user("globo_query")
    pxgrid.authorize_for_service(service)

    radius_failures = pxgrid.service_req("getFailures")
    for failure in radius_failures["failures"]:
        print(f"\nID/user: {failure['id']}/{failure['userName']}")
        print(f"Timestamp: {failure['timestamp']}")
        print(f"Reason: {failure['failureReason']}")


if __name__ == "__main__":

    # User must supply a CLI argument of the service for subscription
    if len(sys.argv) < 2:
        print("usage: python query_radius.py <service>")
        sys.exit(1)

    # Pass the service into main() for submission. Example:
    # com.cisco.ise.radius, com.cisco.ise.session, etc
    main(sys.argv[1])
