#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Deletes existing network objects from the FTD sandbox.
Check out the API explorer at "https://<ftd_host>/#/api-explorer"
"""

import json
import requests
from auth_token import get_token


def main():
    """
    Execution begins here.
    """

    # The FTD sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/firepower/
    api_path = "https://10.10.20.65/api/fdm/latest"
    token = get_token(api_path)

    # To authenticate, we issue a POST request with our username/password
    # as a JSON body to obtain a bearer token in response.
    del_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Load the currently-configured network objects, which is populated
    # by the "get" script. These will be targets for deletion
    with open("json_state/present_netobjs.json", "r") as handle:
        network_objs = json.load(handle)

    # Iterate over the loaded objects and issue DELETE requests for each
    for net in network_objs:
        del_resp = requests.delete(
            net["links"]["self"], headers=del_headers, verify=False
        )

        # Print object details if success or error fails if failed. We
        # don't wait to raise_for_status() which halts the entire process
        # even if a single element fails
        if del_resp.ok:
            print(f"Deleted {net['name']} network object at {net['id']}")
        else:
            print(f"Couldn't delete {net['name']} network object at {net['id']}")
            print(f"  Details: {del_resp.status_code} / {del_resp.reason}")


if __name__ == "__main__":
    main()
