#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Script to collect WSA web transactions using the SMA API.
"""

from datetime import datetime
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
        "startDate": "2016-09-30T18:00:00.000Z",
        "endDate": "2018-10-31T19:00:00.000Z",
        "filterBy": "proxy_services",  # other options: socks_proxy, l4tm
        "filterOperator": "is",
        "offset": 0,
        "limit": 20,
        "device_type": "wsa",
        "orderBy": "timestamp",
        "orderDir": "desc",
        "transactionStatus": "all",
    }

    # Collect web transactions matching the query parameters
    web_transactions = sma.req("web-tracking/web_transaction", params=params)

    # Create the column names for the CSV file
    text = "timestamp,url,src_ip,bw_kbps,wbrs_score,status\n"
    outfile = "web_report.csv"

    # Iterate over each web transaction, extract the attributes sub-dictionary
    for web_transaction in web_transactions["data"]:
        attr = web_transaction["attributes"]

        # Convert timestamp from integer (eg 1524768840)
        timestamp = datetime.fromtimestamp(attr["timestamp"])

        # Add in the 6 key fields. Note that the direction may be blank
        # when one of the appliances (ESA or WSA) generates an email locally.
        # Also, expand the recipient list using a colon between entries
        text += f"{timestamp},{attr['url'][:80]},"
        text += f"{attr['srcIP']},{attr['bandwidth']},"
        text += f"{attr['wbrsScore']},{attr['transactionStatus']}\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
