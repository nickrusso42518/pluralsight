#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using the Cisco Meraki REST API to create/update
webhooks. The webhook data is read in from a JSON file,
and this script automatically trigger test webhooks.
"""

import os
import time
import json
from meraki_helpers import get_network_id, req


def main(org_name, net_name):
    """
    Execution begins here.
    """

    # Find the network ID for the specified org and network
    net_id = get_network_id(net_name, org_name)

    # Load in the webhooks to add from the JSON file
    with open("add_webhooks.json", "r") as handle:
        webhooks = json.load(handle)

    # For each webhook to add
    for webhook in webhooks:

        # Add each webhook server individually
        print(f"adding webhook '{webhook['name']}'")
        if not webhook["url"].lower().startswith("https"):
            print(" url is not 'https', skipping")
            continue
        add_http = req(
            f"networks/{net_id}/httpServers", method="post", jsonbody=webhook
        ).json()

        # Print JSON structure of response for troubleshooting
        # print(json.dumps(add_http, indent=2))

        # Send a test webhook to each server based on URL
        # after waiting a few seconds to reduce race condition likelihood
        print(f"testing webhook '{webhook['name']}'")
        test_http = req(
            f"networks/{net_id}/httpServers/webhookTests",
            method="post",
            jsonbody={"url": webhook["url"]},
        ).json()

        # Ensure the webhooks are enqueued (ie, started successfully)
        if test_http["status"] != "enqueued":
            raise ValueError(f"webhook creation failed: {test_http['status']}")

        # Wait until the state changes from "enqueued"
        while test_http["status"] == "enqueued":

            # Print JSON structure of response for troubleshooting
            # print(json.dumps(test_http, indent=2))

            # Rewrite "test_http" to update the status every few seconds
            time.sleep(2)
            test_http = req(
                f"networks/{net_id}/httpServers/webhookTests/{test_http['id']}",
            ).json()

        # The final status should be "delivered"; if not, raise error
        # For additional confirmation, check the webhook receivers too
        if test_http["status"] != "delivered":
            raise ValueError(f"webhook delivery failed: {test_http['status']}")

    # Collect the current webhooks and print them as confirmation
    net_http = req(f"networks/{net_id}/httpServers").json()
    print(f"Current webhook receivers for {net_name}:")
    print(json.dumps(net_http, indent=2))


if __name__ == "__main__":
    # Get the org name from the env var; default to DevNet
    org = os.environ.get("MERAKI_ORG_NAME", "DevNet Sandbox")

    # Get the network name from the env var; default to DevNet
    net = os.environ.get("MERAKI_NET_NAME", "DevNet Sandbox Always on READ ONLY")

    # Pass in org and net name arguments into main()
    main(org, net)
