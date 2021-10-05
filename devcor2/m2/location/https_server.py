#!/usr/bin/env python

"""
Author: Nick Russo (original work by Cory Guynn, see README)
Purpose: Simple HTTPS server to receive HTTP requests from Meraki
to track location data for wireless clients.
"""

import json
from flask import Flask, json, request


# Define constants for Meraki-supplied validator, user-defined
# secret, and specific API version used (2.0 currently newest)
VALIDATOR = "c8b77133f4bd2218df387186212a6e946d5b4207"
SECRET = "globo123!"
VERSION = "2.0"


# Create flask app object
app = Flask(__name__)


@app.route("/", methods=["GET"])
def process_get():
    """
    Meraki first sends an HTTP GET to collect the validator. This is
    presented in the Meraki UI and needs to be returned so Meraki can
    determine tenancy. It is returned as plain text in the HTML body.
    """
    return VALIDATOR


@app.route("/", methods=["POST"])
def process_post():
    """
    Meraki then sends periodic HTTP POSTs representing location data
    for each client. This functions simply prints it to stdout in
    a nice JSON format to ensure Meraki is working.
    """

    # Ensure the data is valid JSON and has the "data" key present
    data = request.json
    if not data or not "data" in data:
        return ("Incorrect JSON formatting or missing 'data' key", 400)

    # Ensure shared secret presented by Meraki matches ours
    secret = data["secret"]
    if secret != SECRET:
        msg = f"Mismatched secret, saw {secret}, expected {SECRET}"
        print(msg)
        return (msg, 401)

    # Ensure API version presented by Meraki matches ours
    version = data["version"]
    if version != VERSION:
        msg = f"Mismatched version, saw {version}, expected {VERSION}"
        print(msg)
        return (msg, 400)

    # Simply print the data out in pretty JSON format. More professional
    # solutions could write these entries to a remote database
    print(json.dumps(data, indent=2))

    # Return number of observations (items) seen so our test client
    # can perform some additional data integrity checking
    return ({"num_observations": len(data["data"]["observations"])}, 200)


if __name__ == "__main__":
    # Supply valid certificate and key so flask can run HTTPS. You must
    # use the fullchain.pem and not the cert.pem if using letsencrypt.
    cert = "/etc/letsencrypt/live/your.domain.com/fullchain.pem"
    key = "/etc/letsencrypt/live/your.domain.com/privkey.pem"
    app.run(host="0.0.0.0", debug=True, ssl_context=(cert, key))
