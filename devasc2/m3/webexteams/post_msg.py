#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Webex Teams REST API using the
public Cisco DevNet sandbox. Be sure to export the following
environment variable before running this script:

export WT_API_TOKEN=<paste token here>
"""

import os
import requests


def main():
    """
    Execution begins here.
    """

    # Edit this depending on the message you want to post, and
    # in which room (also called a "space") you want to post it.
    TEXT_TO_POST = "Posted via Cisco Webex Teams REST API!"
    ROOM_NAME = "Globomantics"

    # Basic variables to reduce typing later. The API path is just the
    # always-on Webex Teams sandbox in DevNet. Webex Teams was formerly
    # known as Cisco Spark and I expect the URL to be updated at some
    # point to reflect the new name.
    api_path = "https://api.ciscospark.com/v1"

    # Once you sign up for Webex Teams and login, you can get your bearer
    # token here: https://developer.webex.com/docs/api/getting-started
    # The token is supplied as the value of an Authorization header.
    # If you don't export the WT_API_TOKEN environment variable, a
    # ValueError is raised with a usage message (good error checking)
    bearer_token = os.environ.get("WT_API_TOKEN")
    if not bearer_token:
        raise ValueError("Use 'export WT_API_TOKEN=<token>' to access API")
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Perform a GET request to get a list of all rooms in which you are
    # a member. This includes all types of rooms (private, group, etc.)
    get_rooms = requests.get(f"{api_path}/rooms", headers=headers)

    # If GET request fails, raise HTTPError, otherwise get list of rooms
    get_rooms.raise_for_status()
    rooms = get_rooms.json()

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(rooms, indent=2))

    # Perform a basic linear search to find the specified room.
    # Print out the room name and title and store the room ID, which is
    # a large, complex string.
    internal_room_id = None
    for room in rooms["items"]:
        if ROOM_NAME.lower() in room["title"].lower():
            print("Room information")
            print(f"  Title: {room['title']}")
            print(f"  ID: {room['id']}")
            internal_room_id = room["id"]
            break

    # Assuming we found the room, issue a POST request to send the specified
    # message into the specified room. The "body" dict has to specify
    # the room ID (discovered by the previous GET request) and the text
    # we want to post.
    if internal_room_id:
        body = {"roomId": internal_room_id, "text": TEXT_TO_POST}
        post_resp = requests.post(
            f"{api_path}/messages", headers=headers, data=body
        )
        # If POST request fails, raise HTTPError, otherwise get data about post
        post_resp.raise_for_status()
        log = post_resp.json()

        # Debugging line; pretty-print JSON to see structure
        # import json; print(json.dumps(log, indent=2))

        # Assuming the POST was successful, print out the text actually posted
        # along with the email address of the poster, which should be you.
        print(f"\nMessage '{log['text']}' posted by '{log['personEmail']}'")


if __name__ == "__main__":
    main()
