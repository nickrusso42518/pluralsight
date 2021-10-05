#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco ACI REST API using the
public Cisco DevNet sandbox to list current endpoint groups (EPG).
"""

import requests


def main():
    """
    Execution begins here.
    """

    # Basic variables to reduce typing later. The API path is just the
    # always-on ACI simulator in DevNet. The body represents a nested dict
    # to generate a token and requires a JSON string. These login credentials
    # are available here, be sure to check for updates:
    # https://developer.cisco.com/site/aci/
    api_path = "https://sandboxapicdc.cisco.com/api"
    body = {"aaaUser": {"attributes": {"name": "admin", "pwd": "ciscopsdt"}}}

    # The ACI sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # Perform a POST request with the basic login information to get a token.
    # The ACI API will consume JSON from the body for login. Then, extract
    # the token from the large JSON structure that is returned.
    auth_resp = requests.post(
        f"{api_path}/aaaLogin.json", json=body, verify=False
    )

    # If HTTP POST fails, raise HTTPError, otherwise get JSON body
    auth_resp.raise_for_status()
    auth = auth_resp.json()

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(auth, indent=2))

    # Extract token from within the JSON structure
    token = auth["imdata"][0]["aaaLogin"]["attributes"]["token"]

    # For future authentication, the token must be supplied inside of a header
    # named "APIC-Cookie=<token>", so build a dict using that information.
    # In this case, we are collecting a list of ACI endpoint groups (EPGs).
    headers = {"Cookie": f"APIC-Cookie={token}"}
    epg_resp = requests.get(
        f"{api_path}/class/fvAEPg.json", headers=headers, verify=False
    )

    # If HTTP POST fails, raise HTTPError, otherwise get JSON body
    epg_resp.raise_for_status()
    epgs = epg_resp.json()

    # Debugging line; pretty-print JSON to see structure
    # import json; print(json.dumps(epgs, indent=2))

    # The API call above returns a list of dics, so iterate over the list
    # contained in "imdata" and extract the "dn" (the distinguished name)
    # and current configuration state from each dict.
    print(f"EPGs found: {epgs['totalCount']}")
    for epg in epgs["imdata"]:
        print(f"  Name: {epg['fvAEPg']['attributes']['dn']}")


if __name__ == "__main__":
    main()
