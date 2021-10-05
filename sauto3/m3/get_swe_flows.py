#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect and display the SWE flows.
"""

from cisco_sw_enterprise import CiscoSWEnterprise


def main():
    """
    Execution starts here.
    """

    # Access the SWE sandbox and collect flows from a specific IP
    swe = CiscoSWEnterprise.devnet_reservable()
    flows = swe.get_flows_from_ips(
        last_n_minutes=30, limit=20, source_ips=[]
    )

    # Create the column names for the CSV file
    text = "start_t,end_t,prot,src_ip,src_port,dst_ip,dst_port,pkts,bytes\n"
    outfile = "swe_flow_report.csv"

    # Iterate over each flow
    for flow in flows:

        # Create dict with short keys to make accessing the key
        # pieces of data easier
        data_fields = [
            flow["statistics"]["firstActiveTime"][:19],  # trim after "."
            flow["statistics"]["lastActiveTime"][:19],
            flow["protocol"],
            flow["subject"]["ipAddress"],
            str(flow["subject"]["portProtocol"].get("port", "N/A")),  # int
            flow["peer"]["ipAddress"],
            str(flow["peer"]["portProtocol"].get("port", "N/A")),
            str(flow["statistics"]["packetCount"]),
            str(flow["statistics"]["byteCount"]),
        ]

        # Combine all elements into a comma-separated list with newline
        text += f"{','.join(data_fields)}\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")

    # Delete cookie when complete
    swe.logout()


if __name__ == "__main__":
    main()
