#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collects and saves ARP table details from each distribution
device into a single CSV file for archival. Currently requires a
reservation and VPN connection into the new DevNet NSO sandbox.
"""

from operator import itemgetter
import requests


def main():
    """
    Execution begins here.
    """

    # Basic variables to reduce typing later. At this time, there is not
    # a NSO always-on DevNet instance, so this is an example from a
    # reserved sandbox. As such, the IP addressing in the URL may change.
    # This will use RESTCONF, not the proprietary REST API.
    api_path = "https://10.10.20.49/restconf/data"

    # Disable obnoxious SSL verification warnings for the sandbox
    requests.packages.urllib3.disable_warnings()

    # Basic authentication (no tokens) works for our simple example
    basic_auth = ("developer", "C1sco12345")

    # For HTTP GET, we need to accept a variety of YANG data encoded as JSON.
    # This technique joins all the list elements together with a comma to
    # create a single, comma-delineated string value for the Accept header.
    accept_list = [
        "application/vnd.yang.api+json",
        "application/vnd.yang.datastore+json",
        "application/vnd.yang.data+json",
        "application/vnd.yang.collection+json",
    ]
    get_headers = {"Accept": ",".join(accept_list)}

    # Define table columns first, separated by commas. This will be the first
    # line written into the CSV spreadsheet with ARP entries to follow
    arp_table = "device,ip_addr,mac_addr,interface,age\n"

    # Loop over the selected devices, in this case, the distribution devices.
    # Intentionally including a bogus device so we can handle the failure "softly"
    for device in ["dist-rtr01", "dist-rtr02", "bogus"]:

        # Build a device-specific URL in case we want to add more requests
        # later (collect more stats, etc)
        device_url = f"{api_path}/tailf-ncs:devices/device={device}"

        # Use HTTP GET to get ARP stats from the device. Note that HTTPS
        # is used now, so disable SSL verification
        get_resp = requests.get(
            f"{device_url}/live-status/tailf-ned-cisco-ios-stats:arp",
            auth=basic_auth,
            headers=get_headers,
            verify=False,
        )

        # Anything other than 200 is failure, so just skip that device
        if get_resp.status_code != 200:
            print(f"Could not collect {device} ARP stats; skipping")
            continue

        # Request succeeded; store address list for use later
        addr_list = get_resp.json()["tailf-ned-cisco-ios-stats:arp"]["address"]

        # Optional debugging statement to view JSON body of ARP entries
        # import json; print(json.dumps(get_resp.json(), indent=2))

        # Iterate over all addresses in the address list
        for addr in sorted(addr_list, key=itemgetter("interface")):

            # Append new "row" to the table with ARP details
            arp_table += (
                f"{device},"
                f"{addr['ip']},"
                f"{addr['hardware-addr']},"
                f"{addr['interface']},"
                f"{addr.get('age-mins', '-')}\n"
            )

    # All ARP entries have been concatenated to the arp_table text.
    # Open the file and write all the text at once; minimize disk writes
    outfile = "arp_stats.csv"
    with open(outfile, "w") as handle:
        handle.write(arp_table)

    # Use this handy "column" command to quickly view the file,
    # or download to view it Excel or other spreadsheet software
    print(f"Use 'column -s, -t {outfile}' to view from shell")


if __name__ == "__main__":
    main()
