#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Used to create a test pxGrid user to confirm that
the SDK works without any service lookups/subscriptions.
"""

from pxgrid import PxGrid


def main():
    """
    Execution begins here.
    """

    # Instantiate a new PxGrid object to the DevNet sandbox (10.10.20.70)
    pxgrid = PxGrid("ise24.abc.inc")

    # Activate a new user for this integration
    pxgrid.activate_user("globo_test")


if __name__ == "__main__":
    main()
