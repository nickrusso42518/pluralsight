#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Watch for suspicious application on the Globomantics network.
This will generate alerts when matching traffic is seen.
"""

from cisco_sw_enterprise import CiscoSWEnterprise


def main():
    """
    Execution starts here.
    """

    # Access the SWE sandbox and collect flows from a specific IP
    swe = CiscoSWEnterprise.devnet_reservable()

    # Assemble the HTTP body representing the app. Specifically, it measures
    # traffic from a specific IP going to a destination protocol/port
    # This flow DOES appear in the traffic generator, but randomly ...
    body = {
        "name": "Wired Brain Coffee",
        "description": "Detects suspicious app on the Globomantics network",
        "subject": {
            "ipAddresses": {"includes": ["209.182.177.5"]},
            "orientation": "either",
        },
        "peer": {"portProtocols": {"includes": ["43283/TCP"]}},
    }

    # Add the event, enable it, and confirm it was enabled
    # No need to store body data; nothing else to process
    swe.add_custom_event(event_body=body, enable=True)

    # Delete cookie when complete
    swe.logout()


if __name__ == "__main__":
    main()
