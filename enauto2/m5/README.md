# Implementing Location Scanning and Event-driven Alerts
This directory contains many scripts to setup/test Meraki webhooks:
  * `add_webhooks.json`: List of dictionaries which specifies a webhook name
    and target. Each one should be added to Meraki.
  * `build_webhooks.py`: This adds new webhooks, starts a webhook test,
    and waits for a result.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
