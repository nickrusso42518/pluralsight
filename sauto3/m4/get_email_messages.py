#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Script to collect ESA email messages using the SMA API.
"""

from cisco_sma import CiscoSMA


def main():
    """
    Execution begins here.
    """

    # Instantiate new CiscoSMA object using dCloud parameters
    sma = CiscoSMA()

    # Query parameters to specify the scope of search. These timestamps were
    # specified in the documentation and (surprisingly) work well for testing
    params = {
        "startDate": "2018-01-01T00:00:00.000Z",
        "endDate": "2018-11-20T09:36:00.000Z",
        "ciscoHost": "All_Hosts",
        "searchOption": "messages",
        "offset": 0,
        "limit": 20,
    }

    # Collect email messages matching the query parameters
    emails = sma.req("message-tracking/messages", params=params)

    # Create the column names for the CSV file
    text = "timestamp,direction,subject,icid,sender,recipients\n"
    outfile = "email_report.csv"

    # Iterate over each email and extract the attributes sub-dictionary
    for email in emails["data"]:
        attr = email["attributes"]

        # Add in the 6 key fields. Note that the direction may be blank
        # when one of the appliances (ESA or WSA) generates an email locally.
        # Also, expand the recipient list using a colon between entries
        direction = attr["direction"]
        text += f"{attr['timestamp']},{direction if direction else 'N/A'},"
        text += f"{attr['subject']},{attr['icid']},"
        text += f"{attr['sender']},{':'.join(attr['recipient'])}\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
