#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Using NETCONF with operational state YANG models to enable
streaming telemetry to the Elastic (formerly ELK) stack in Docker.
This is an example of dial-in model-driven telemetry (MDT).
"""

import logging
from logstash import TCPLogstashHandler
from ncclient import manager
from lxml.etree import fromstring
import xmltodict


def main():
    """
    Execution begins here.
    """

    # Define basic logging parameters. This script writes JSON-formatted
    # MDT messages directly to logstash without a broker like kafka (simpler).
    logger = logging.getLogger("netconf_mdt")
    logger.setLevel(logging.INFO)

    # Define logstash connection parameters to reach the ELK stack container.
    # It uses logstash v1 format on TCP port 5045 per the logstash config.
    logstash_params = {"host": "elk.njrusmc.net", "port": 5045, "version": 1}
    logger.addHandler(TCPLogstashHandler(**logstash_params))

    # Define NETCONF connection parameters to reach the Cisco always-on IOS-XE
    # latest code sandbox as a demonstration.
    netconf_params = {
        "host": "ios-xe-mgmt-latest.cisco.com",
        "port": 10000,
        "username": "developer",
        "password": "C1sco12345",
        "hostkey_verify": False,
        "allow_agent": False,
        "look_for_keys": False,
        "device_params": {"name": "csr"},
    }

    # Connect to the device and disconnect when scope ends
    with manager.connect(**netconf_params) as conn:

        # Add YANG-based xpath filters to this list to subscribe to multiple
        # topics. Be sure to check the proper YANG model for your version!
        xpaths_desired = [
            "/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds",
            "/memory-ios-xe-oper:memory-statistics/memory-statistic",
        ]

        # For every xpath in which to subscribe ...
        for xpath in xpaths_desired:

            # Issue the establish-subscription RPC via helper function
            sub_resp = telemetry_subscribe(conn, xpath)

            # Print raw XML RPC-reply for troubleshooting
            # print(sub_resp.xml)

            # Convert the RPC-reply to a Python dict so we can test the
            # subscription result and reveal any errors
            sub_json = xmltodict.parse(sub_resp.xml)
            sub_result = sub_json["rpc-reply"]["subscription-result"]["#text"]

            # Print JSON representation of XML RPC-reply
            # import json; print(json.dumps(sub_json, indent=2))

            # Ensure RPC succeeded by checking the 'subscription-result' key
            if "ok" in sub_result.lower():
                # Success text: "notif-bis:ok". Print subscription ID also
                sub_id = sub_json["rpc-reply"]["subscription-id"]["#text"]
                print(f"Subscribed to '{xpath}' via ID: {sub_id}")
            else:
                # Example of an error: "notif-bis:error-no-such-option"
                print(f"Could not subscribe to '{xpath}'. Reason: {sub_result}")

        # Subscriptions complete. Next, loop forever to wait for notifications
        while True:

            # This blocks until a notification is received
            msg_xml = conn.take_notification()

            # Print raw XML notification for troubleshooting
            # print(msg_xml.notification_xml)

            # Convert XML into Python objects (JSON-like) for logstash
            msg_json = xmltodict.parse(
                msg_xml.notification_xml, postprocessor=str_to_int
            )

            # Send an INFO log to logstash carrying MDT dict as extra data.
            # Also convert any integer values from strings to simplify graphs
            sub_id = msg_json["notification"]["push-update"]["subscription-id"]
            logger.info(sub_id, extra=msg_json)

            # Print terse message indicating a notification logged
            timestamp = msg_json["notification"]["eventTime"]
            print(f"Logged update from ID {sub_id} at {timestamp}")

            # Print JSON representation of XML notification
            # import json; print(json.dumps(msg_json, indent=2))


def str_to_int(path, key, value):
    """
    Helper function that automatically converts all strings to
    integers, assuming it is possible. This avoids complex
    logstash filtering which would need to be customized for
    each notification, also requiring docker to rebuild the image
    everytime a new xpath filter is added. Use as 'postprocessor'
    with the xmltodict.parse() function.
    """
    try:
        return (key, int(value))
    except (ValueError, TypeError):
        return (key, value)


def telemetry_subscribe(conn, xpath, period=1000):
    """
    Simple helper function to subscribe to periodic telemetry events. Issues
    the 'establish-subscription' RPC with the specified xpath and period.
    This is easily extended to support dampening period as well. This
    option was omitted for simplicity.
    """

    # Extract these strings to keep the multi-line string clean
    xmlns = "urn:ietf:params:xml:ns:yang:ietf-event-notifications"
    xmlns_yp = "urn:ietf:params:xml:ns:yang:ietf-yang-push"

    # Build RPC text by substiting XML and xpath variables
    subscribe_rpc = f"""
        <establish-subscription xmlns="{xmlns}" xmlns:yp="{xmlns_yp}">
            <stream>yp:yang-push</stream>
            <yp:xpath-filter>{xpath}</yp:xpath-filter>
            <yp:period>{period}</yp:period>
        </establish-subscription>
    """

    # Issue the RPC by forming the proper XML from the RPC string,
    # and return the RPC-reply
    subscribe_resp = conn.dispatch(fromstring(subscribe_rpc))
    return subscribe_resp


if __name__ == "__main__":
    main()
