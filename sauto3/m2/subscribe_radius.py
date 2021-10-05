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
    pxgrid.activate_user("globo_listen")
    pxgrid.authorize_for_service(service, ws_subscribe=True)


if __name__ == "__main__":

    # User must supply a CLI argument of the service for subscription
    if len(sys.argv) < 2:
        print("usage: python subscribe_radius.py <service>")
        sys.exit(1)

    # Pass the service into main() for submission. Example:
    # com.cisco.ise.radius, com.cisco.ise.session, etc
    main(sys.argv[1])
