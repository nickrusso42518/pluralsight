# Module 3 - Collecting Client Health Details from Cisco DNA Center
This directory contains two relevant DNA Center API examples:
gathering the high-level client health and detailed client health
data by MAC address.

## Client health summary
This section includes two Python scripts:

  * `get_client_health.py`: Collects high-level client health and prints
    the output in a human-readable form.
  * `get_client_health_timeout.py`: Same as the previous script, except
    adds support for a timeout/attempts mechanism to demonstrate one method
    for handling API timeouts.

## Client details
This section includes two Python scripts:

  * `get_client_detail.py`: Requires a list of MAC addresses via command-line
    argument, then iteratively checks the client detaisl for each MAC. It
    prints the wireless health in a human-readable form.
  * `get_client_detail_throttle.py`: Same as the previous script, except
    adds rate-limiting support to stay in complaince with the DNA Center
    rate limits. HTTP requests that exceed the rate-limit are not processed.

## Supporting files
The `auth_token.py` file contains the `get_token()` function
to re-use this common code between all scripts. It reduces
copy/paste and promotes DRY (don't repeat yourself).

The `data_ref/` directory contains files which reveal the
JSON structure of HTTP responses coming back from DNA Center:

  * `get_client_detail.json`: Example output from the `client-detail`
    HTTP GET request to DNA center.
  * `get_client_health.json`: Example output from the `client-health`
    HTTP GET request to DNA center.
  * `req_throttle.json`: Example of the HTTP 429 HTTP response body
    to detail what this rate-limit errors looks like.

There are two shell scripts used to test the client health API
calls as these Python scripts require MAC addresses to be supplied
as command line arguments:

  * `test_clients.sh`: Passes several known-present MAC addresses into
    `get_client_detail.py`. This script does not have built-in rate
    limiting and will raise an HTTP 429 "Too Many Requests" error.
  * `test_clients_throttle.sh`: Same as previous script except uses
    `get_client_detail_throttle.py`. This script adds rate-limiting
    and functions correctly.
