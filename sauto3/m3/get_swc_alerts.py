#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect and display the SWC alerts.
"""

from cisco_sw_cloud import CiscoSWCloud


def main():
    """
    Execution starts here.
    """

    # Create new SWC object from environment variables
    swc = CiscoSWCloud.build_from_env_vars()

    # Get the current SWC alerts (watchlist triggers, etc)
    alerts = swc.req("alerts/alert/")
    for alert in alerts["objects"]:

        # Print a two-line summary including the time, type, and description
        print(f"{alert['created']}: {alert['type']}")
        print(f"Details: {alert['description']}\n")


if __name__ == "__main__":
    main()
