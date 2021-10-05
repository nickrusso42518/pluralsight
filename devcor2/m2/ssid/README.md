# Meraki SSID Management
This directory contains scripts to collect basic information about
SSIDs in the public Meraki sandbox, as well as provide a simple mechanism
to enable or disable a specific SSID.

## Python code
There are three Python files:

  * `get_ssids.py`: Collects a list of SSIDs within the DevNet network
    and prints their basic details in a human-readable format.
  * `change_ssid_state.py`:  Enables or disables a specific SSID by number.
    These are supplied as command-line arguments.
  * `meraki_helpers.py`: Contains helper functions to simplify authentication
    and searching for the DevNet organization and network. This code is very
    similar to the Meraki demonstrations from previous (beginner) courses.

## Reference files
The `json_ref/` directory contains examples of the HTTP response bodies
that may come back from some of the HTTP requests sent:

  * `get_ssids.json`: List of dictionaries representing the full list of
    SSIDs within a given network.
  * `change_ssid_state_3_0.json`: Details from SSID 3 after changing
    "enabled" to false.
  * `change_ssid_state_3_1.json`: Details from SSID 3 after changing
    "enabled" to true.
