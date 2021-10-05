#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using RESTCONF via requests to configure MDT subscriptions.
"""


import sys
import requests
from yaml import safe_load


def main(hosts):
    """
    Execution begins here.
    """

    # Ignore any obnoxious warnings about SSL validation for this test
    requests.packages.urllib3.disable_warnings()

    # Load the generic subscriptions for all devices
    with open("vars/mdt.yml", "r") as handle:
        data = safe_load(handle)

    # Define HTTP headers to specify JSON-encoded YANG data will be used
    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json, application/yang-data.errors+json",
    }

    # Build the HTTP body outside the loop as it is the same for all hosts
    mdt_body = build_mdt_body(data)

    # Optional debugging statement to see the JSON body
    # import json; print(json.dumps(mdt_body, indent=2))

    # Iterate over hosts supplied by CLI args
    for host in hosts:

        # Issue an HTTP PUT request to add the new subscriptions in
        # an idempotent way
        config_resp = requests.put(
            f"https://{host}/restconf/data/Cisco-IOS-XE-mdt-cfg:mdt-config-data",
            headers=headers,
            json=mdt_body,
            auth=("cisco", "cisco"),
            verify=False,
        )
        config_resp.raise_for_status()

        print(f"Added ({len(data['subscriptions'])}) subscriptions to {host}")


def build_mdt_body(data):
    """
    Given the data loaded from disk, this function returns the
    properly-formatted JSON body for the RESTCONF POST/PUT request
    that adds/updates MDT subscriptions.
    """
    sub_list = []
    for item_id, sub in data["subscriptions"].items():

        new_sub = {
            "subscription-id": item_id,
            "base": build_base_dict(sub),
            "mdt-receivers": {
                "address": sub["rx"]["ip"],
                "port": sub["rx"]["tcp_port"],
                "protocol": "grpc-tcp",
            },
        }
        sub_list.append(new_sub)

    full_body = {"mdt-config-data": {"mdt-subscription": sub_list}}
    return full_body


def build_base_dict(sub):
    """
    Given the specific subscription data, this function determines
    whether a subscription is periodic or on-change, and adds
    the proper key/value pairs to the HTTP body JSON dictionary.
    """
    base_dict = {
        "stream": "yang-push",
        "encoding": "encode-kvgpb",
        "xpath": sub["xpath"],
    }
    if sub["period"] == "on_change":
        base_dict["no-synch-on-start"] = False
    else:
        base_dict["period"] = sub["period"]

    return base_dict


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python restconf_mdt.py <host1> ... <hostN>")
        sys.exit(1)

    main(sys.argv[1:])
