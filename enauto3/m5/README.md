# Monitoring Network Health and System Events with DNA Assurance
This directory contains the files needed to monitor DNA center
using health checking and event notifications (webhooks).

Relevant files:
  * `get_health.py`: Runs the site, network, and client health checks,
     then saves their outputs to individual files in `outputs/`.
  * `build_webhook.py`: Creates a new webhook using `webhook.site` to
    capture DNA center assurance notifications.

**Note:** Check the `data_ref/` directory for example JSON responses from all
API calls.
