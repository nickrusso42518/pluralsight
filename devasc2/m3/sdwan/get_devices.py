#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco SD-WAN REST API using the
public Cisco DevNet sandbox.
"""

import requests


def main():
    """
    Execution begins here.
    """

    # Basic variables to reduce typing later. The API path is just the
    # always-on SD-WAN API (really, vManage) sandbox in DevNet.
    # IMPORTANT: You can see the full list of API calls using on-box
    # API documentation here: https://sandboxsdwan.cisco.com:8443/apidocs
    api_path = "https://sandboxsdwan.cisco.com:8443"

    # The SD-WAN sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # These credentials are supplied by Cisco DevNet on the sandbox page.
    # These specific parameters may change, so be sure to check here:
    # https://developer.cisco.com/sdwan/learn/
    login_creds = {"j_username": "devnetuser", "j_password": "Cisco123!"}

    # Create a single TCP session to the SD-WAN sandbox. This allows the cookies
    # and other state to be re-used without having to manually pass tokens around.
    # We can perform regular HTTP requests on this "sess" object now.
    sess = requests.session()
    auth_resp = sess.post(
        f"{api_path}/j_security_check", data=login_creds, verify=False
    )

    # An authentication request has failed if we receive a failing return code
    # OR if there is any text supplied in the response. Failing authentications
    # often return code 200 (OK) but include a lot of HTML content, indicating a
    # a failure. If a failure does occur, exit the program using code 1.
    if not auth_resp.ok or auth_resp.text:
        print("Login failed")
        import sys
        sys.exit(1)

    # At this point, we've authenticated to SD-WAN using the REST API and can
    # issue follow-on requests. Next, we collect a list of devices. Assuming
    # the request worked, iterate over the list of devices and print out
    # the device IP address and hostname for each device.
    device_resp = sess.get(f"{api_path}/dataservice/device", verify=False)
    if device_resp.ok:
        devices = device_resp.json()["data"]

        # Debugging line; pretty-print JSON to see structure
        # import json; print(json.dumps(devices, indent=2))

        print(f"Devices managed by DevNet SD-WAN sandbox:")
        for dev in devices:
            print(f"Device IP: {dev['system-ip']:<12} Name: {dev['host-name']}")


if __name__ == "__main__":
    main()
