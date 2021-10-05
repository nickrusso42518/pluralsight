#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
perform basic user/group and auditlog management.
"""

import sys
import getpass
from datetime import datetime, timezone
from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # Before trying to add users, first determine if our current
    # user has administrative privileges. If not, exit
    if not sdwan.is_admin():
        print("You are not currently authenticated as an 'admin' user")
        sys.exit(1)

    # We have admin privileges; create a new group named "audit" which has
    # all device-level read/write permissions
    group_name = "audit"
    body = {
        "groupName": group_name,
        "tasks": [
            {
                "feature": "Audit Log",
                "read": True,
                "enabled": True,
                "write": False,
            },
            {
                "feature": "Interface",
                "read": True,
                "enabled": True,
                "write": False,
            },
            {"feature": "System", "read": True, "enabled": True, "write": False},
        ],
    }

    # Create the "unit" group based on the body defined above
    sdwan.add_user_group(body)

    # Create a new user Jane Doe and add her to the "audit" group
    sdwan.add_user("jdoe", "jane doe", [group_name])

    # Update her password using interactive user input (secured)
    user_password = getpass.getpass("Enter password for jdoe: ")
    sdwan.update_password("jdoe", user_password)

    # Create a new SD-WAN object to log in as the new user
    audit = CiscoSDWAN(
        host="10.10.20.90", port=8443, username="jdoe", password=user_password
    )

    # Collect the audit log using the new user just created
    audit_resp = audit.get_audit_log()

    # Store log entries in a CSV file for easy viewing (security auditors
    # love CSV files). Can also access via GUI here in DevNet sandbox:
    # https://10.10.20.90:8443/index.html#/app/monitor/auditlog
    outfile = "log_useraudit.csv"
    print(f"Creating '{outfile}' from vManage audit log")
    with open(outfile, "w") as handle:
        handle.write("dtg,device,user,msg\n")
        for log in audit_resp.json()["data"]:
            dtg = datetime.fromtimestamp(log["entry_time"] // 1000, timezone.utc)
            device = log.get("logdeviceid", "none")
            user = log.get("loguser", "none")
            msg = log.get("logmessage", "none")
            handle.write(f"{dtg},{device},{user},{msg}\n")
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
