# Cisco Firepower Threat Defense (FTD) REST API
This directory contains examples of using HTTP GET, POST, and DELETE
REST API calls to the Cisco DevNet FTD reservable
sandbox.

## Source code
There are several Python files:

  * `auth_token.py`: This collects a bearer token from FTD which can be
    used for future API calls.
  * `get_netobjs.py`: Collects a list of current network objects and
    writes a summary to `stdout` as well as saves them to a JSON file
    `json_state/present_netobjs.json`.
  * `get_netobjs_pages.py`: Same as `get_netobjs.py` except introduces
    pagination techniques.
  * `add_netobjs.py`: Adds individual network objects as defined in
    the JSON file `json_state/new_netobjs.json`. Duplicates are
    ignored and an error message is displayed (does not crash program).
  * `delete_netobjs.py`: Deletes individual network objects as defined in
    the JSON file `json_state/present_netobjs.json`. Duplicates are
    ignored and an error message is displayed (does not crash program).

## JSON files
The `json_state/` directory contains two files:

  * `new_netobjs.json`: Contains a JSON list of dictionaries representing
    network objects to be added. Consumed by `add_netobjs.py`
  * `present_netobjs.json`: Contains a JSON list of currently-configured
    network objects. Generated by `get_netobjs.py` and
    `get_netobjs_pages.py` and consumed by `delete_netobjs.py`.
