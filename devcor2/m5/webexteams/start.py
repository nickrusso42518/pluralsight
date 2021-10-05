#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

import os
import requests
from flask import Flask, render_template, request
from database import Database

# Create Flask object
app = Flask(__name__)

# Load database from JSON file
db = Database("data/initial.json")


@app.route("/wtwebhook", methods=["POST"])
def process_wtwebhook():
    """
    The Webex Teams API will target this URL for webhooks, which are
    always HTTP POST requests carrying specific data about the event
    that triggered them.
    """

    # Dangerous, no error checking for brevity
    bearer_token = os.environ.get("WT_API_TOKEN")

    # Print JSON details of received webhook for debugging
    # import json; print(json.dumps(request.json, indent=2))

    # The text is considered sensitive information, so perform
    # a GET request to retrieve the text containing the account ID
    api_path = "https://api.ciscospark.com/v1"
    get_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }

    # Issue HTTP GET for the message ID provided by the webhook,
    # and store the text from it. Example text: "globobot acct100"
    # If it fails, just quit early.
    msg_id = request.json["data"]["id"]
    get_resp = requests.get(
        f"{api_path}/messages/{msg_id}", headers=get_headers
    )
    if not get_resp.ok:
        return "no message"

    # Print JSON details of GET request for debugging
    # import json; print(json.dumps(get_resp.json(), indent=2))

    # Take the last word of whatever was included in the message
    # and grab the account ID
    msg_text = get_resp.json()["text"]
    acct_id = msg_text.split(" ")[-1]

    # Perform regular account ID lookup and app logging
    acct_balance = db.balance(acct_id.upper())
    response_str = f"balance for {acct_id}: {acct_balance}"
    app.logger.debug(response_str)

    # To make the bot reply, issue an HTTP POST containing the account
    # balance for the specific query. If it fails, just quit early.
    room_id = request.json["data"]["roomId"]
    body = {"roomId": room_id, "text": response_str}
    post_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}",
    }
    requests.post(f"{api_path}/messages", headers=post_headers, json=body)
    return "complete"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This is a view function which responds to requests for the top-level
    URL. It serves as the "controller" in MVC as it accesses both the
    model and the view.
    """

    # The button click within the view kicks off a POST request ...
    if request.method == "POST":

        # This collects the user input from the view. The controller's job
        # is to process this information, which includes using methods from
        # the "model" to get the information we need (in this case,
        # the account balance).
        acct_id = request.form["acctid"]
        acct_balance = db.balance(acct_id.upper())
        app.logger.debug(f"balance for {acct_id}: {acct_balance}")

    else:
        # During a normal GET request, no need to perform any calculations
        acct_balance = "N/A"

    # This is the "view", which is the jinja2 templated HTML data that is
    # presented to the user. The user interacts with this webpage and
    # provides information that the controller then processes.
    # The controller passes the account balance into the view so it can
    # be displayed back to the user.
    return render_template("index.html", acct_balance=acct_balance)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
