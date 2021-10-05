#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and test its Real-time Monitoring API methods.
"""

import json
from datetime import datetime, timezone
from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()
    with open("sys_stat_query.json", "r") as handle:
        query = json.load(handle)

    # Issue the request to collect CPU/memory util using query
    sys_stat_resp = sdwan.get_system_stats(query)

    # Debugging statement to see data response
    # print(json.dumps(sys_stat_resp.json(), indent=2))

    # Write output to CSV file. This could be written to a time-series
    # database and fed into a telemetry system, which is basically what
    # vManage GUI is doing with the data.
    outfile = "log_cpumem.csv"
    print(f"Creating '{outfile}' from vManage system stats")
    with open(outfile, "w") as handle:
        handle.write("dtg,cpu util%,mem util%\n")
        for stat in sys_stat_resp.json()["data"]:
            dtg = datetime.fromtimestamp(stat["entry_time"] // 1000, timezone.utc)
            cpu = round(stat["cpu_user_new"], 2)
            mem = round(stat["mem_util"], 2)
            handle.write(f"{dtg},{cpu},{mem}\n")
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
