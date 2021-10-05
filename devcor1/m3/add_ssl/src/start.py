#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way. This builds on
previous revisions by adding a MySQL database in another Docker container.
"""

import os
from flask import Flask, render_template, request
from database import Database


# Create Flask object
app = Flask(__name__)

# Initialize a MySQL database towards the other container
db = Database("mysql://root:globomantics@db/db", "data/initial.json")


@app.before_request
def before_request():
    """
    Called before HTTP request is processed. Opens the connection to the DB.
    """
    db.connect()
    app.logger.debug("Connected to db")


@app.after_request
def after_request(response):
    """
    Called after HTTP request is processed. Close the connection to the DB.
    The "response" parameter provides access to the HTTP response but in our
    case, it isn't relevant, so just return it.
    """
    db.disconnect()
    app.logger.debug("Disconnected from db")
    return response


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
    # Identify the certificate and key as a 2-tuple
    ctx = ("../ssl/cert.pem", "../ssl/key.pem")
    app.run(
        host="0.0.0.0", debug=True, use_reloader=False, ssl_context=ctx
    )
