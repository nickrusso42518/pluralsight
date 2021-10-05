#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate how to create event subscriptions using REST webhooks
on Cisco DNA center via API calls.
"""

import time
from dnac_requester import DNACRequester


def main():
    """
    Execution begins here.
    """

    # Create a DNARequester object with our sandbox parameters
    dnac = DNACRequester(
        host="10.10.20.85", username="admin", password="Cisco1234!", verify=False
    )

    # Collect a list of all assurance-related events, allowing event-driven
    # monitoring of our network (telemetry)
    events = dnac.req(f"dna/intent/api/v1/events", params={"tags": "ASSURANCE"})

    # Debugging statement to see event list structure
    # import json; print(json.dumps(events.json(), indent=2))

    # Build a list of event IDs to pass into the webhook request body.
    # Could use a JSON file, but showing a more direct approach for diversity
    event_ids = [event["eventId"] for event in events.json()]
    body = [
        {
            "name": "globo_assurance",
            "subscriptionEndpoints": [
                {
                    "subscriptionDetails": {
                        "connectorType": "REST",
                        "name": "webhook.site",
                        "description": "Great for testing",
                        "method": "POST",
                        "url": "https://webhook.site/0b43c29f-8e0c-4ae4-9b3f-9f1df76dcaf8",
                    }
                }
            ],
            "filter": {"eventIds": event_ids},
        }
    ]

    # Create the new webhook
    add_resp = dnac.req(
        f"dna/intent/api/v1/event/subscription", method="post", jsonbody=body
    )

    # Debugging statement to see add response
    # import json; print(json.dumps(add_resp.json(), indent=2))

    # Webhook processing is consistently fast; use a simple, naive solution.
    # You can optionally build a more robust "wait" system if you like.
    time.sleep(5)

    # Trim leading '/' from URL as the DNAC object handles that already, then
    # ask DNAC for a status update on this specific webhook creation
    add_status = dnac.req(add_resp.json()["statusUri"][1:]).json()

    # Debugging statement to see status response
    # import json; print(json.dumps(add_status, indent=2))

    # If an error message exists, raise a ValueError with the status message
    if add_status["errorMessage"]:
        raise ValueError(add_status["statusMessage"])

    # Otherwise, just print the status message along with the status indicator
    print(f"{add_status['statusMessage']} / {add_status['apiStatus']}")

    # Collect a list of all subscriptions. At this time, there is no way to query
    # a specific subscription, so collect them all
    subs_resp = dnac.req(f"dna/intent/api/v1/event/subscription")

    # Subscriptions are sorted by oldest first, newest last, so extract the
    # last element in the list using a slice
    my_sub = subs_resp.json()[-1]

    # Debugging statement to see newly-added subscription
    # import json; print(json.dumps(my_sub, indent=2))

    # Print simple confirmation message with subscription ID, which is
    # necessary for future deletion
    print(
        f"Confirmed {my_sub['name']} using ID {my_sub['subscriptionId']}"
    )


if __name__ == "__main__":
    main()
