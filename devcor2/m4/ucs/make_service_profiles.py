#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Cisco UCS Manager for creating a service profile
from an existing template using the "UCS Management" DevNet
sandbox (requires reservation).
"""


import requests
import xmltodict

# The number of service profiles (logical servers) to create from the template
NUM_SP = 3


def main():
    """
    Execution starts here.
    """

    # Create login credentials as string containing XML, issue
    # API call to login, and extract cookie for subsequent requests
    login_body = '<aaaLogin inName="ucspe" inPassword="ucspe"/>'
    login_resp = ucs_manager_api(login_body)
    cookie = login_resp["aaaLogin"]["@outCookie"]

    # Create the XML body that instantiates new service profiles from
    # a pre-existing service profile template named "ls-globotemplate".
    # Each service profile begins with "SP" and is suffixed by a number,
    # starting from 1 and counting up to the "NUM_SP" constant. If those
    # numbers aren't available, it just keeps counting higher.
    sp_body = f"""
    <lsInstantiateNTemplate
        dn="org-root/ls-globotemplate"
        cookie="{cookie}"
        inTargetOrg="org-root"
        inServerNamePrefixOrEmpty="SP"
        inNumberOf="{NUM_SP}"
        inHierarchical="no">
    </lsInstantiateNTemplate>
    """.strip()
    sp_resp = ucs_manager_api(sp_body)

    # Iterate over the new service profiles added
    for sp in sp_resp["lsInstantiateNTemplate"]["outConfigs"]["lsServer"]:
        print(f"Added SP with DN {sp['@dn']} and ID {sp['@intId']}")


def ucs_manager_api(body):
    """
    Performs an API call to the DevNet UCS manager in the DevNet sandbox.
    The body should be a string containing valid XML content for whatever
    action the caller wants to run.
    """

    # Issue HTTP POST to perform login using the XML body defined above.
    # The API almost always returns HTTP 200, so raising HTTPError is unlikely.
    # Also, the API path and headers are fixed, although sandbox IP may change
    post_resp = requests.post(
        "http://10.10.20.113/nuova",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=body,
    )
    post_resp.raise_for_status()

    # Print API response to see structure as raw XML useful for learning
    # print(post_resp.text)

    # Convert XML into JSON
    post_resp_json = xmltodict.parse(post_resp.text)

    # Print API response as parsed JSON, which can be accessed via Python
    # import json; print(json.dumps(post_resp_json, indent=2))

    return post_resp_json


if __name__ == "__main__":
    main()
