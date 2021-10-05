# ChatOps with Webex Teams
This directory contains a simple "chatops" implementation using
Webex Teams and the Globomantics CRM app.

## Flask modifications
The CRM app has been stripped down in this demonstration as it
does not use a remote SQL database or HTTPS (SSL certificates).
Using these would complicate the demo and draw attention away
from "chatops". The setup is almost identical to the basic CRM
app explored in the previous course.

A new `process_wtwebhook()` function has been added to `start.py`
to accept the HTTP POST webhook from Webex teams. This function
is mapped to the `/wtwebhook` URL, the webhook target. The
function performs an HTTP GET to get the potentially sensitive
text from the message using the globobot's token then uses an
HTTP POST to reply on the globobot's behalf with the account balance.

Because the CRM app is making HTTP requests on behalf of the globobot,
the `WT_API_TOKEN` environment variable must be exported in the shell
that runs the CRM app. This should be the API token for the globobot.

## New code
The `webhook/` directory contains the `add_webhook.py` file which
creates a new webhook that listens for any new messages that mention
the globobot. This triggers an HTTP POST to the CRM app. Just like with
Webex Teams demos in previous courses, `WT_API_TOKEN` must be exported.

The `webhook/json_ref/` directory contains several JSON examples
of HTTP body text that is useful for reference:

  * `add_webhook.json`: The response from the HTTP POST request after
    successfully adding a webhook.
  * `get_bot.json`: The response from the HTTP GET request after getting
    users that match the globobot's "email" address.
  * `get_msg_details.json`: The response from the HTTP GET request
    sent from the CRM app to get the potentially sensitive text from
    the message that triggered the webhook.
  * `webhook_body.json`: The HTTP POST request body within the webhook
    sent from Webex Teams to the CRM app.

Also included are two simple Bash scripts used to manage the webhooks.
Both require that the `WT_API_TOKEN` is exported:

  * `delete_webhook.sh`: Deletes a webhook by ID (first CLI argument).
  * `get_webhook.sh`: Gets a list of all current webhooks.

## Using ChatOps
To get the balance for a specific account, you must target the
globobot and include the account ID. The account ID must be
the last word in the text message. Valid examples:

  * `@globobot acct100`
  * `@globobot hi, what is the balance for acct200`

These examples will not work: 

  * `@globobot I need the acct100 balance` because the `acctid` will
    be the string "balance".
  * `@globobot hi, what is the balance for acct300?` because the
    `acctid` will be the string "acct300?".

