#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a new webhook to integrate Webex Teams with
our existing CRM app. An older version of the app is used
for speed and simplicity (local file DB and HTTP only).
Be sure to export the following environment variable before
running this script:

export WT_API_TOKEN=<paste token here>
"""

import os
import requests


def main():
    """
    Execution begins here.
    """

    # Basic variables to reduce typing later. The API path is just the
    # always-on Webex Teams sandbox in DevNet. Webex Teams was formerly
    # known as Cisco Spark and I expect the URL to be updated at some
    # point to reflect the new name.
    api_path = "https://api.ciscospark.com/v1"

    # The token is supplied as the value of an Authorization header.
    # If you don't export the WT_API_TOKEN environment variable, a
    # ValueError is raised with a usage message (good error checking)
    bearer_token = os.environ.get("WT_API_TOKEN")
    if not bearer_token:
        raise ValueError("Use 'export WT_API_TOKEN=<token>' to access API")
    get_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }

    # To ensure the bot only activates when we mention it, we must add
    # a filter using the bot's "person ID". This is NOT the same as the
    # bot ID from the app page.
    get_resp = requests.get(
        f"{api_path}/people",
        headers=get_headers,
        params={"email": "globobot@webex.bot"},
    )
    get_resp.raise_for_status()

    # Print JSON details of GET response for debugging
    # import json; print(json.dumps(get_resp.json(), indent=2))

    # Extract the bot's ID and build the HTTP body for creating a webhook
    bot_id = get_resp.json()["items"][0]["id"]
    webhook_data = {
        "name": "crm",
        "targetUrl": "http://crm.njrusmc.net:5000/wtwebhook",
        "resource": "messages",
        "event": "created",
        "filter": f"mentionedPeople={bot_id}",
    }

    # Issue an HTTP POST request to build a new webhook with the body above
    post_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }
    post_resp = requests.post(
        f"{api_path}/webhooks", headers=post_headers, json=webhook_data
    )
    post_resp.raise_for_status()

    # Print JSON details of POST response for debugging
    # import json; print(json.dumps(post_resp.json(), indent=2))

    webhook_id = post_resp.json()["id"]
    print(
        f"Webhook for {webhook_data['targetUrl']} added with ID\n{webhook_id}"
    )


if __name__ == "__main__":
    main()
