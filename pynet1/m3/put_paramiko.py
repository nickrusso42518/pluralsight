#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via paramiko to configure network devices.
"""

import time
import paramiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    1 second for the command to be processed. Sometimes this has to be
    increased, can be very tricky!
    """
    output = conn.send(command + "\n")
    time.sleep(1.0)
    return output


def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and
    decode the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["host_list"]:

        # Load the host-specific VRF declarative state
        with open(f"vars/{host['name']}_vrfs.yml", "r") as handle:
            vrfs = safe_load(handle)

        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(
            f"templates/paramiko/{host['platform']}_vpn.j2"
        )
        new_vrf_config = template.render(data=vrfs)

        # Create paramiko SSH client to connect to the device
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=host["name"],
            port=22,
            username="pyuser",
            password="pypass",
            look_for_keys=False,
            allow_agent=False,
        )

        # Start an interactive shell and collect the prompt
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        # Send the configuration string to the device
        print(new_vrf_config)
        send_cmd(conn, new_vrf_config)
        print(f"Updated {host['name']} VRF configuration")
        conn.close()


if __name__ == "__main__":
    main()
